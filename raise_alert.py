import pprint
def raise_alert(time, src, URL, val):

    BARLINE = "------------------------------"

    print(BARLINE)
    print("[!] executed time: {}".format(time))

    print(BARLINE)
    print("[!] executed script:")
    print(src)

    print(BARLINE)
    if URL != None:
        print("[!] detected URLs:")
        for url in URL:
            print(url)
    
    print(BARLINE)
    print("[!] detection reason: ", end='')

    val["results"] = sorted(val["results"].items(), key=lambda i: i[1], reverse = True)
    
    k = val["results"][0][0]
    if k == "detect_iex":
        print("IEX detected.")
    elif k == "detect_url":
        print("URL detected.")
    elif k == "detect_sign":
        print("Abnormal amounts of symbols detected.") 
    elif k == "detect_unreadable_string":
        print("Abnormal amounts of unreadable strings detected.")
    elif k == "detect_strings_blacklist":
        print("suspicious words detected.")
    else:
        print()

    print(BARLINE)

    # 評価確認用
    print("[!] Suspiciousness: {}".format(val["totalscore"]))
    pprint.pprint(val["results"])

    print(BARLINE)
