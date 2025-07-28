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
        'SID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7MPa7wz_LPxvDVVzDaZjL0wACgYKAf4SARYSFQHGX2MiyTUQ7QXjl7s3a9uwfMS3lxoVAUF8yKpHIVg9pG-VGA-nU53lBDdR0076',
        '__Secure-1PSID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7XEef04TjMlgH3RPvFaVG_gACgYKAd4SARYSFQHGX2MinPZasfMXgN6AFLJmrL1lvRoVAUF8yKpbAUb4i7Ruufd3hVK3EHUk0076',
        '__Secure-3PSID': 'g.a000zgiGjxQ17mQFEYXquUwyYNDuM1F2VePuGJC7aaw2PkiMker7qJmg5shRPakuOA-vZX-0lgACgYKAf8SARYSFQHGX2MiBdyXrszkEaNmWJJk0xQsqxoVAUF8yKp0qil1YCZ_BYOg6Rqw_Mwz0076',
        'HSID': 'AOXPxduUrKQaPZ3E7',
        'SSID': 'A10Z9sFaohEdfM0Ki',
        'APISID': 'mTncr2CBzLZRbBgh/A_fCwEM6JRScGBMGz',
        'SAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        '__Secure-1PAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        '__Secure-3PAPISID': 'ZysW6ufdp1i4o0Ae/AC7raX2DeR48oQ52h',
        'NID': '525=CqaCWtzyyzUjVS2NDunmO4dyIeuL70ROfMxnIejR5SlSkdggG5QbTvpToyKCKzbCXMgouHEp6-xeaO5mZJfPHegK63R5_phhSEuE8q-wayCtClKg8k-nxpWohdjjWJuFEVELNhlOxNONN3XcphVvo2hUKw5OiWsozmEhe08tmVkri729Wuv0-9wyAAqswg1ZX0DU-eLIXEZMGgaQ_XA4JRlXs4Di5l1cA2t-i8LCPYvqQT6WHvdKDIt43WPEaNuZrhSHATlAHjok3V88WWJocPHyFNc_hZ-DTXVcJTdsOmkQHwBecArQN1wceUGTCC5pZFOaVAdjiRAW9pqVboVWwURnVdfAlzxvd2ITOGTNA73dCb_pFI8DDfYyFo36pAxCjCl05MlXFC9AsA_SZLdfDdHY8VvNWTQE7Y-iECneNZdQgQvioLW8aMNvv4btgAYjKSbCfYmUuOnqZFDnarxadPEFEhoweT4W8Ip5bGPDP9Pxep7uHAzT0tWmm8001yhpWkv1T8AgOo-91k4HuBRpQn16cP3YsMNpVQhYgJOpb1q6PvMtUNFOK8kp0dWJoChpVVTf3PilR8jURjPUMXO93pJVmVbQ2TtI3J4oZlaVd9vntoAKFETjOHfbXbMESfjLOH4yGBPMbQQTMWlx5hcYUx51A5eC4dvoIL_jNqRHO1RtRtXmaGtDDE1DFEV46otddj1vM_AMnYtsZkQ_bLXL7Mb6uegVuKz5R9vb3DgGHx5rldoL_k-XnuxlXWnpv9A8FYAdohbxCI3c2RFntrbS9pfQFnGHSKTk8tnQLQdMqYl3YtdCPSmLy7_DSYVcya824jABFYlMzGs3t8SLS95kOtvwvWy4W9H9b9FT9lES0rwavbkcJeclQaZdoah2cPASxmrMIogqTLw2DG46m2eP6YZ9HcPA1CNCblBt-WkHkURuL1rVrmV37TIX2nI8AJiCcTt76Qu9chowEbB7d_iZCt2RPUs9vybNHWD2GE4bt3zV6F_yD1G9fJMT3NicZdYRkke04C5RQHh0v098A2uuBPuYvRRU-SxMZRUpBLlnMUQhTuILYRD6BVNXWn0IXQNe9VQKWm3g-SzJRDX4EucXQm0RE7WjmLJ4SWJLsR0oMqnNOiHx5NtdlYzYksI5xv4UZi4RiuPs',
        '__utma': '207539602.2100594883.1742201890.1753707908.1753729226.9',
        '__utmc': '207539602',
        '__utmz': '207539602.1753729226.9.9.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'S': 'billing-ui-v3=VZdxgpJFHhtpnWtX9gWpFEAHZ-B87svk:billing-ui-v3-efe=VZdxgpJFHhtpnWtX9gWpFEAHZ-B87svk',
        '__utmb': '207539602.4.9.1753729275346',
        'SIDCC': 'AKEyXzVQwRvGBJGZngqGpc69_5eyEvWTpZtT_mrzN_NFp69jkK1nhXy_hTGM3yJT-vZypPmKLQ',
        '__Secure-1PSIDCC': 'AKEyXzU6gMYCmPSJhLtjfIKuaZDwcx0HSFSCoyprsg-ONSWQw7jHbR0DcxSwjN1eSaw5CA_G0uk',
        '__Secure-3PSIDCC': 'AKEyXzW4bSGdl3gv9sJHV_X4sd_1LFlpgWDZ601nTAI2k3NJjnvFYJVIh5_aR-EYFSALgduURHA',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager?tc=96%2C87&wst=1753729217557&cst=1753729222801&si=7827306353864165&pet&sri=2&hmi=false&ipi=nig1b96um9im&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_zckbkop89of30&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByCmn9iv1Acg9acEYgDAAgD4AwE%3D&spul=500&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_zckbkop89of30',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'nig1b96um9im',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '7827306353864165',
        'style': ':m2',
        'cst': '1753729222801',
        'wst': '1753729217557',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '3',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2NK3AJMApd556WVzWX6EQpXg4qBwQ:1753729225471',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329zQoUe5I+EjYo7lUV9c/wrEWq3EjgrIJOczPMy8mezyww1jAwxjEmioPZNOkrzvV9rBtlAMtxTtX4rdYeX1ToLlcNloreUGj1iHVmuXe6cJkYxscr30ao78GChuOOFt0/FF1D9PSjYQ8AO3K07S4MZOWEB4L01eewpgbMJlnZrDbo9M4YadDb5TwLjRGsl+weVwimFFYTb3DIg2bwjhJUQzBdcSyABsSb+K16LIREJFSdmfiLD9/9WdV9dD9k6yMbyQ6eFyU",null,[null,[null,null,null,["!Pj2lPWXNAAa73VJ7m91CJHDnseBfzO47ADQBEArZ1BgIaT6hhpo91CGXwDy46hiIb15_12e-ALu9rGsCc-IB3HGY1_CZnyHrPNbST50-AgAABc9SAAAAKmgBB34ATBXbpINJSx1hvlcbkoEbwfu-fCCxqAhKIA3uOjOZ9AP4tFIAReTWKx8Iv1AWmyLpnvpHI_jY8LvtdaQ1Fdmp3p8Q_lSZlZsCeN3VvoiZCemv3XGf6S44BU8ZwAbIomajVCO-8VqXlCImInhYb_4idMa68f4SPPBYsNaJ_h5eg2QiZ6GyuoOSqXMeJlDcBKnZZ3TPYn9MpJVX1QgbNbkzDCqimiX5VOSA3lR3dNoPmPP5X0K0M6HLt94zAJRIwGuKu1NR_m3GvpqdEhPUcrO_qGTHw1T58wYx989WcGW1LzXdjy-57aN2btalHVtPLO6HcIWmIB37hZhavRb-wC6L5xea29DR8payPJnSlgnwdvMMYpdFh6HarUr0nkcu1gBa1PETphY7xhJ1gEgq3X8exfmyAyrHxLPzrgreKPqaKpDAt0My39DUbVCwnjgEA-epKifkt9oU8TbCQBBrqan_kGLV3RoUD6QOmk5vG-SnPBBXmMjYnacHaPL8D5wS4ZuoiwBQkEeD1vsuX7TBdrDbd5rFZ6Am7LTc7fg0gEnLlCf45h3F9DiZndWfdHythyVkMphcvzYCAArLowpH3CbA65-pCkQYGdjiLYQ0OhFTPmYiZsAGxZdtzpoUzZDEqccBWN9lw8tGJDQvyQMPkKOgZA6l2cMKQunTV6lK3qUrQHITIk_fU2q3kLzrEAnlY6iTmZnaMgIrBFz7pR5PJz3wX5JDASBAQ7AYAg4cKWR1Ngq5R3GCkTLbivvuoyNzi6UYXrEDM5_dpfKZFKsBYYoALe5OvcMUtdak5oej3zWTKMilhChWZnFJCEWF-3g_3DPCqwj_G3Y9a9DnRtE7DZI6UH01dEGEpg1pGBuC5CYE8oCOO6u9GTlg87jnxkNapYu6oieCYD_5MWglawJpnp1JhQ-tEnjt9Sa36tFiknACOaApOTCgvjtYtB1AYDfSa1ph1qJtA-eC-Hq6Czt3IAjQ-ZiesVjLEX8-8BnzYZXfGbKg8ZYuo9VWTLrXselld7wrDkY2GxaW7Oe3uAA3XeZ0C6elZ6_QdUcCmV72v3TgQaGRZKNr7x5RZs3GgyEfcBACBorJhYcYvPZdcq-z6oKeCh1T9Nn23ue0FP_HGZEFrkXoweN02FBj5gR0bw17FofIHfYYHHn8MRQ8yw1u5JcXANKzThC5zf5pI5xc2RsUK6k-BEx0dxaO3Z-XJU-INjeVjf5uUC3nUe4XpPRu2siGrBry66roal4s1-ugmA1gB8w9EA_ExlciC7r4IcqbvbC95heYWye691tH9P6L-Z14NcA4lUcb2q2BKT8AhBrMfAz5tbvIZa9d1Dqzp0kAfnwF-sOZziFYo5TnktXy0AbyJ9qzyQkTnYL-DY8eL9m2bl5huE3qIFPExb0nylYp3_YHB_O6_0IseYpssMZdZUMVpsEKW8hAkNVLhayhlHPNBdak-_gpJwrePCYo50QS9S1UIRfS4flSq5HZBEipgbXb5mothDDmT0qJkZMJFMpEC04tHGIUx9D6g4zsO2mlAoN0gg2Zb9xd8AOzS16xx7oGvpewV-yNqiwWjkX9fVC24EvcDQXFHsGgzQuq3iJIrR4Ymn9NLhmY6bCdRq10u8oY2sH82UanW0PUMgzJ1C5UAcr8DKb6W3FdzP-sYatKFM1fNsGsRW0KpaSXWERq0FMdtoAgVP64vpKMFwJLtXwrGbOVkpRwZnpKz0_1LMnQ0gEgunLSrHXck2DH35MNusU5PNjy0If-lm0nOpZeTPgaaK54iXG4CtdXjpIoj6qtPUeZGE_S7qPNXCI9GpZOhI6JpitLz4jFoOucwBszccRs8Y2yvc8adSSQUCc01UIstB3YDBImQG8k5GBLOlUFFpgEkM_l62DdyhXzjtX5VjT4Dw9csvselV6XzVBqVo5isfXzQhlhWLiC8DMd-VD_2klWI7h7o9sjx4J__XIeS_tdUjhm8gSc56uHBceOJ7DbURWFRr0gtpvLXCMhmiJcFbU5_WY8L1CS-4rrH2tP-_2m-S6tJcyNNONIusYk04FZeXSeTPX0qGAKqEV1lRRhKv39uazi0stCr9Ef6hoqqXQqnT2QtPhzXGmRZXkXcwd1RoWkpwMmerSBEcC-A75B7QwTdwh3nOO5Re4wkNrDXyOsnumwqNlnTX1H0iryG5ENuG0Rgrlp0HTndfgH57ardHzMFpPf3k7h4RIgci1DzlnQzBEoODUdl2USdmr57wsTgD3FlwLTemgok--6u9NMSnSHoGWLeGCU4gkgWnTskgOputKhM9iBDSAiJ5cmr_NiyQ18tSffyRYez1jt1WxHMJegXNJToXvtoHw6jOVU3B01H6d_oY8XLonsAMogj3P1GoyAsNYh_WY6SAZ6q1sDiw7UlL75n8siqOQehHX7hs7mZLl4-4Ktz-uXssm7AMt1n3NMA2poJqL_z-h3fYYYfaNRfdFRM9poqv_InNGM1G-3mz7r0qS6ubAuMS-gvwRwCL4zQXp4uslRjyz_qO7bUqwKbDUCP0l12E-pZIkffrehq5YgqQz-4gePTOGbYtwrnTi0NWDkB5IbDNFVDlgeCr_K-GP-SkhOxe36HJmlmWYyHt9CsLNDmODvmtBYi9TNj6F1R6PTuzdzGfoSncnb_X26ytawckc1VJu4FnKtQkJylb9Mz4jZjEtEdOXCpCYQBXPK4TrJMinlefSt0h32zHetyn07OCO7GovspcY7fA2k5F2W7IMTMtLdVxvBEPQ9fL1Y2ZMMm1Kc1817msPLog5szm8wVpJykACqNdTY2azdhLChE8ge4ddhWVDKAevHPsGCJEqE_dSLV_7GFaRpNiY8cbGhUZ-Ig3tVu0S5H99t6DInphSNBjUvZHEesyZTu9qNyDDqpjHwv82UZUSyB4cWdESDqhBDaI3DkjyI4BpFByaH0l72xZjvrOzY_VCWC7vCOcD1b7yeStYzoiG0AgUVRz0JIY-LqybSFdgURD06fFq-Wr8rIBiWWN0ZpLuBz6Qa6_LsgE7XXIQ2DyXUZYldnEEANL3Sfp0GekU58kx8pgh_0HdxIhv-MwjJJFtPNLzrd0lqrxsYo20ugyihZKIjC-A9kbtLwuHoigSvlZ7f-q0fWHB_lSx2t-7lQ7OVSEtPHiYSyswpDNPUR8-EA_foa-ZxW2akhXGK8A3s1strQocbXeBVxynEA-oFauUKpLBfW1AGU7KGTZ5QmQmK1CSfRnwmZadRyRp96Ffahr4ygeVRqmrY4aw4Y1AguRisP_giJpPilcIBEpGq4vvZdgZS8Gi4-mJf9OPQn_tOyuSVAX7IM4906axwZUpalQXVq9WzzYF2bEcsiXQegK_Bm3wWKkdQVXBuW2kXxuRybvYwuGquFqsu5cPK1-rJJDxV1KH1BSXPo9Hwi0xUr98gaLYTkw983J4_jHXKHXp3N3eINrQwnDy0h_Pb81unn3p3FbWjV9OWMQwhAKKn0q-PXWc4uXGdARQW8huszg"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"4248",null,"__s7e_data__61bb463a","Mia Reid",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAEQAxogEgJVUxoDVVNEMAhAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,3,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,1,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,1,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 2028KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,1,"Mozilla2f5.0 2028Linux3b Android 103b K29 AppleWebKit2f537.36 2028KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 0023a003a00 GMT2b0200 20282a48424a2a 20343142 20234831482827 2027443133454a29,770c67fc,2,7:a21,3,19852685320,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,36d:a40,"f,1985268568d,"n,0,0,"t,198526848fe,0,0,0,0,19852684909,19852684909,19852684909,19852684909,19852684909,0,1985268491c,19852684b83,19852684bc8,19852684ba1,1985268536b,1985268536b,19852685755,1985268585a,1985268585b,198526858a1:a10:a31,3,"h,1,"p,b5,87,"m,12e,2475,353,f56,a60,df9,f47,f9e,329,2658,4abc'
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
