def score(data):
    weights = {
        'detect_iex': 100,
        'extract_url' : 20,
        'detect_sign' : 250,
        'unreadable_string' : 400,
        'detect_strings_blacklist':1,
        'logistic_reg':100
    }

    scores = 0

    detect_iex = boolToint(data["detect_iex"]) * weights["detect_iex"]
    scores += detect_iex

    extract_url = len(data["extract_url"]) * weights["extract_url"]
    scores += extract_url

    detect_sign = data["detect_sign"] * weights["detect_sign"]
    scores += detect_sign

    unreadable_string = data["unreadable_string"] * weights["unreadable_string"]
    scores += unreadable_string
    
    detect_strings_blacklist = 0
    for a in data["detect_strings_blacklist"]:
        detect_strings_blacklist += a['score'] * weights["detect_strings_blacklist"]
    scores += detect_strings_blacklist

    logistic_reg = data["logistic_reg"] * weights["logistic_reg"]
    scores += logistic_reg
    
    return {"totalscore":scores,
            "results": {"detect_iex":detect_iex,
                        "extract_url":extract_url,
                        "detect_sign":detect_sign,
                        "unreadable_string":unreadable_string,
                        "detect_strings_blacklist":detect_strings_blacklist,
                        "logistic_reg":logistic_reg}} 
    
def boolToint(x):
    if(x == True):
        return 1
    else:
        return 0
