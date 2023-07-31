import re

def concat_strings(input_str, debug=False):
    original_len = len(input_str)

    if debug:
        print(input_str)

    pattern = r'''(['"])((?:(?<=\\)\1|(?!\1).)*?)\1\s*\+\s*(['"])((?:(?<=\\)\3|(?!\3).)*?)\3'''
    regex = re.compile(pattern)

    while True:
        matches = regex.search(input_str)
        if matches is None:
            break

        replaced_str = regex.sub(lambda m: m.group(1) + m.group(2) + m.group(4) + m.group(1), input_str)
        input_str = replaced_str
        if debug:
            print(input_str)

    if debug:
        print(input_str)
    if debug:
        print("Original string length:", original_len)
        print("Final string length:", len(input_str))

    return input_str