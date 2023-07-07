import re
def remove_backtick(src):
    removed_backticks_src = src
    pat3 = re.compile(r"`([^0abefnrtuv])")
    removed_backticks_src = re.sub(pat3,'\\1',src)
    return removed_backticks_src