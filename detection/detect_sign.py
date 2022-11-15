import re
def detect_sign(src):
    #Detect the rate of symbols (too high -> obfuscated ->malicious)
    p = re.compile('[^\s0-9a-zA-z]|`')
    sign_num = len(re.findall(p, src))
    src_len = len(src)
    ret_val = sign_num / src_len

    if src_len < 100:
        return 0
    if ret_val < 0.3:
        return 0
    return ret_val
