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
        'NID': '525=EDZnOOZEfK9IJxYyhq8--EsvOv93m_-1R_Uqmf3c5Dno-FKAhQ16o6agofkp9T69bm7VAE_dz_uAaXPx8EoBdAw-HrURaKkNL8ElBYhW71MNjVhLuu7w40eDFT6m3ENf5e8QHBFGZZ6JbGeZGVDctVzZexZM1WRphpN534XeqCfAQieEMkLCsEWQQDuldMwovMp7am1_4QY13bZHez-PWUei7nSzmPVZERuD8Fnn3qN8DMeKAL5ZVOtfnKiif8ykNDiBcQklsT-lvqfRC5Gzp158Gf5DgZapRVrPNYRDvlPQFO_d6JSKLGJNo_h3L8RPhyYDL4QYPYHKzrEBUHxVn_t5-ZDDtFvGq1p1pYWxN1s-noQusuA84enJtFJsG93tppxFz4cW6g_IfWvo2DsuiWqlWzs9VeBK4aVrR5wxkgRzYr8DfF_7kV7GZZ6ETMA4IkFyt-Y_evnFU1QveWbyouC4Gt0pjp86oSJTvKNAgRGUr8Czv554JAjmy-7tgLeiGGR4hX7A5SJf58biG7kzUeIMxX3S5VlyJVxickXxAIQm8-pj9ZsPMRdJUr-i8XyL7z3BIivARJh0fkXgBgIDNFReoVU6fjeM1B99CLFlAJTieR9Jy2rhyjJE8va9XDSheMzNe_M8JqI9yZyFNrFnJ93mc1x0Nz972q9-Fu7f1Z1QDVM_xGkTsTRURkK7zRtBlMDQz75OxSVC9FZiu0jXAuZEic0h81Jda_njIXKyyRusQwS0ka24hd78y0JTzJL9smpAmG_9xrpw7ODRstdX-EiNOTzSNkpJYUKHMeyTAy1evg4jtR28tPkhfk6_eTTb5Ds6eROu_nwIoIpgUGp0wQr53QrSpRkTgGVq9Qca874w6HPNUnaGxyavs2JZhCjdg7fTSe-MeSUai2MKj9m65j5w5UgBfa2gN9HBdi1eUUd8rE5V0E-HBIKUSUwF32zci9n6muJ6jDStuG0KUo1zSmbSRsSAh_wGqYebTQDdsBLrg-ZVghNR_fvwlj3sR9WixDLfIus_wVt78ax333k1dnnaO_LFTYfJ062KEWbYmmCddJbNek7SsKJxHIAP44P3K4ZghVcTkrvIsJUuw7KQQnSav5e5dRJQjZ0wZqEpHSwA5lSAYc5Qi-JKs2MN',
        'SID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVuO7pTCPva7sn0FQ8CflwiQACgYKARISARYSFQHGX2MiSCi4FlIgiH7ImzQ11-KzrhoVAUF8yKqY_Aj-Fv9Llkm2VGLmUM2v0076',
        '__Secure-1PSID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVvGuRCcRLadRtFhS36jxKYwACgYKAQgSARYSFQHGX2MirchICEzeFedNhZ0vtxd5xRoVAUF8yKqx-1WHeKOLrqTYTPuLHHRh0076',
        '__Secure-3PSID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVnF8eHO4ja2MLFGecbN_J8QACgYKAYQSARYSFQHGX2MiSVrooXsvS24OZL3irGFBqxoVAUF8yKr4iKExCv1E4FvFM44O-ZXX0076',
        'HSID': 'APJS_TaVdn24EEIBQ',
        'SSID': 'AF8ZM84MsejkY-Pym',
        'APISID': 'MPO5KiSxe2oBoywN/AzBxLLRAFxIkftopS',
        'SAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        '__Secure-1PAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        '__Secure-3PAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        '__utma': '207539602.2100594883.1742201890.1753643295.1753693869.6',
        '__utmc': '207539602',
        '__utmz': '207539602.1753693869.6.6.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        '__utmb': '207539602.5.8.1753693902919',
        'SIDCC': 'AKEyXzW88EIqiNMDtu1c44S0GCLL5xkr8H8wCkUE8SFY8GXe9ntQE8A2c2poiWG0e774HTDy4A',
        '__Secure-1PSIDCC': 'AKEyXzWRVuoQYLOzMiGsWqREL_CvM9je7CCnkNiPElNrQbt7do2zFm5AXdx7-MAQf6i_MlKVA8c',
        '__Secure-3PSIDCC': 'AKEyXzVtOGPQPUYnyZr8JTbkwwIWRSl6WAqWH_IkQFtLnTz798bhq2JMIfHyjYnK5SL8fII7sKQ',
        'S': 'billing-ui-v3=x4QaCJUL-IGRIAS84wc-n84uWyRV1yoz:billing-ui-v3-efe=x4QaCJUL-IGRIAS84wc-n84uWyRV1yoz',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/0/embedded/instrument_manager?tc=96%2C87&wst=1753693850694&cst=1753693866137&si=246936212199323&pet&sri=2&hmi=false&ipi=a2tnxo4pivle&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_k28asla29l040&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByDD7%2FOOvw8g9acEYgDAAgD4AwE%3D&spul=501&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_k28asla29l040',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'a2tnxo4pivle',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '246936212199323',
        'style': ':m2',
        'cst': '1753693866137',
        'wst': '1753693850694',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '7',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2PU60sh9JErZcqDfDy5lycG10YmlQ:1753693868715',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329w4STUlOA9wD2eGEdqyb6E9DmNGHbfK7ITGyLxVw+PNyhfD4bziEIgeywJhANuoIsA8l+jITahijWXbYD6CFSbvVoOJ4z/8HbgE5qtpGq5jt2Av7/LnLZwGJE+7t1Ggfbj+YAylu+U+CnQh4pn7BBCsminnBRsEoR+wwPa4Ju51id4xJR/OItsyxGSVJrWHTkFOqpdQqyAxwf8Vf+pRP4u0X+VJdN63Ih4JlTwRsKlvli6KlHUjTI4vcDssqmRG8U5+dm9t",null,[null,[null,null,null,["!8POl86vNAAa73VJ7m91COPcFFCjPPnk7ADQBEArZ1DLzpb0mv_Ab-cubIptWT2XX0dfddfzo8Q-w8C4vT6_Jj7u1IBVKtfFKf8RZhSJ6AgAABSJSAAAAUWgBB34ATL5ZXKlYjmN3_Tp40mygElBdxj1CCDM73hrtVgkv4WdI0p8IWhtn4Dl7VV3HvYG3zPqYWR64MJqViqaMNi3pPe7glcmtzEE9MEujBc-ZCLIe88Jc0eOPHSelPjfCOxgoTcVFcrnJiVxqMBlIiLLFlutioHjGFLB7-MkPHSM7w5DFTptKFGcknUfzI9DHw2krdOK1_FI8LBKHRMrrWlTanGC-7sFyv-HLYaWNlwQYJE87_valJOZ9POULWbSpPxs1_Ndy7TineESPEjGDRaTgD0LDKj-jzPdvgJY7Qgnu-g5FpnJB9tqlSAGb8fHRCKeaaV-J6NTHxQbJrp4o_9UXNPz_tu54Ha4mlFXxZPBGa9fQCaYyKmbvITeoZ643ZpuqodwkOHKk0rtU3aCqr0m6PuqejX8ud_T3MNP9ybf3Wk3HqmAkidXx_JKHf7tukqRQQe_M81Yo--ab45lxWeXIC6jGcHS3AEsBB5296mTV-xVWw05eNZzibYa5f_QArfwjm8yGiGDDry1rfZnpph6KjW7qFq5kmpDvx_ex0awBdX7bibdlmiIFlnZFwjHbQh86w1rwqK28kOTfLzmhqHQzEa5x1dQEOJQtxp6DJAsQdgDgj2HldZ1xbCTbPCm80L4RGm7MEK-0ZbcoyZsXH3o6_-0Xfo77gF6JP707dX2v-cidkPxP7vrF6-6XjaTIkYJtYMeeHYkzPCyLuj7uGpx3bB6la-sefiCD_PTOyM4xUoVSgu5K6Jdt6aAQqHelxEC94v-H3sQ0-Xo0BP_QDcfMwmNjKQusRx9duqES0SJ3iHM1-KJLh8ZEW6zetB9AfAhz7wR-xU-S01vQwV0eUN4fos3WIxQ-2kJnH9Hq9LjcMdXOObvurWi_q7FNHWD6yZCYKfXcpRcWR1byc8NdPCUIjy1cKd7Dp25j0Hb55A1xjHGjopv3oRQJHs0Ysdw5QIdJJTUguw0hpHeJBI60HvGiimfi_OaLOOnkxVqieTBvfZUZyHmYptSPxbHVZCvqgKw0YEvHOalqtsjUr5U-TAc2OD7VIAjMxO3t5bYbhmQGcoS51UOxrMJs7VkWIue6sOwFQWS6DvfjMm4EwUBLMh33FhyYDINk_fO7F1YrZxp3qOi9PoobqbI5jx1U_9R0Jcn_4C0L_yvVgWAwaGAVsRizTjlirOppdtgKNi0LMo7MWdXP-geRIDBFQfkbO0ZrmSjyvJiU6rzYG-BRsHHYHVYjY3PNjUZ-jhuHtcWkX7p4h4WinES-HtpcgyQ9CZLHkG-HYu2dB8amKHuDDTaKlCfC6hFZEu4JoydCcyhycLxaXt2rDBK_GEKshW8sf-rFJpRAG9ZW941c7aRvAOrx9lW1pHHvQH5igrnmhXvjk6qdlO4S44S9tOAoGYlSb7Z04XlEMPtS21kX_xG1qNzH-8Ax2rFicG6gJ4HImAroG4505sLWoLFbd629Xoo2h4yeO2GJnINC_o9i1OVxNWAdZaMA8c_z_rP-TPelmZMBOye8EDktQ9bk_6Tk4hXdtNShBlo6BVaJK3KquMihppz88RhJ6BnxCKMTCkd0Y_tq4GPllJTuqhakcOoR8Z4L_DNaf_XCeKJWn0N7CzhwUhVi3dd8A0f2S-dNs8pAj1NxIE8Aa57GHVYIx8VqWTf87XEzIV275j2BeKCYg69xuNqQx5EPz90iHSpLREHh9FbwytYcMXlDNJmtDw2XFObEjmt1C5tFlZCzOKdYq48JoyHSTh9DjY9uTTg-Rm7APBTICeLyrZQGRTdohU3eyV9igZiy2CoS3Dscu3J4atvlL7LahBhHSwF5dbQnp9OQnZMKv9RBTEFZ273_Crl6YSQ0fP0iFsTNdfgvjw2w0rJd71f3pFGi9e34ILjKTa_5MdoZC9WtW9sx0hpGSxYOtqi_PjvRH_alPeFD5NdWkWOvI1nD8CqVjSQy8sg88Y9uyJG0kw1LRb7244ZbIgg_Nx1M2GukSa6FiCxq_cRy-bcw_oKuMRH1aZ0djZsdGC4S_LBT2sqcfaw_kMek3yV6A8aGN9MW_W4LNiYqRaAWGyPx2NR4ScDoyUnIkbMxtXEio89kcMkfAQsvE1z9MylysGroKxr8P9f2-aHIOvedI8ttjN0x43xY0YqvlbtxUB4zSbKTISCUJR4d7DXlzD8mCLm8z-YJiTsTOAarJm3D_jtRXnCaWvDViOo95fA8KPMWVZsdUq4zVuIsKol9NGizJxNdC0GCutThHyZi-LUESupFPbpicALtitmawTNlp6PI4w8wsHNjL4gendLhdudyZXJBlfWCoYwgL96q6tvhbRcOVgkAeYMzM8hcbTCmh-1LxOfdx3PiPtbQJWBZZg_8_G3RAdjGnpNDkQYFl6qCDfig2iJ-0hWD0DS5OZTEn7Xh1v8f3TifY5rCkEzrcXl_krPMCQ5TTOeOF_V6vF1MEGia8U5q05ZJHoB8Rc7xfLY9-NCznlEgPeIl_KR_PJaOsnNCDDmwG7LbqzBTTOB6a8cH2I1md6JUFoHk7Jj8GYgNPTMWwO166-hXD1GIfF-OWAda2X8uld6VCUhmxpOF3_v7k5U7I54VRxLEslNZ2L4HaYvLaspJ_qmGpAMNlnf-ej-aXrkonq7JkukKD0hQaeX7uQd2LfQXh0YRI6fFKqJFhfZTPUdiXihp7ryYMT45rjlyA5w1kXgTtHcIIzjYQfxgRubs_IjfToM47Rgi0s5RdUQurtWGaGm344rbNnurRZVd_UmroNnI0KSpjjAqKF93bL7KrrfcW9Ra5b4itrOQ8-sJZjvjWKgyFr2uBtxTzagYowtZL-ZUDtC2--6maKHsJOaUnSR1ByzepCFHdNWbKpIhuvIJWnPLlMTkyUa7bgwK5LloXFq_G5bNCjRGvV_MjvYKTmsxrO_J9WyoI3WRaA7CKv1X3QJgC_g3HbYMZcFnPzfOKRnQdUJSJWIw9pIVcy2os5cuvha3JBFvuS5iMoqOvPNypngXhp3MfgxwMh2EW-drT8_V3-q2I0W4Fnih0MDYJqZYtBqKv0-0P_kzt3YlbyA4AT1WU-mI_byjISmoUv4Pp73rIVI"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",5,2029,null,"3888",null,"__s7e_data__61bb463a","هونجا البونجا",[["US",null,"NY",null,"New York",null,null,null,null,null,null,"10001",null,["Orjreiejejrjdijd","836393"]],null,null,null,"billingAddress",null,null,2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,0,2b6,edd98bac,0,18,4863fd35,1,140,cb2d5c6f,0,2b6,6ad47c6c,1,e8,7bdb49f6,1,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,1,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,1,6:a21,3,198504cd24a,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,28f:a40,"f,198504cd4d9,"n,0,0,"t,198504cc8ff,0,0,0,0,198504cc908,198504cc908,198504cc908,198504cc908,198504cc908,0,198504cc919,198504ccd04,198504ccd3f,198504ccd23,198504cd26a,198504cd26b,198504cd585,198504cd807,198504cd808,198504cd83c:a10:a31,3,"h,1,"p,6d,46,"m,5ff,1411,16b3,1144,219e,923'
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
