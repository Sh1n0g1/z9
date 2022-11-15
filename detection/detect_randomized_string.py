import re

def vowel_rate(str):
  total_vowel = sum(ch in 'aeiouy' for ch in str)
  return float(total_vowel) / float(len(str))

def detect_randomized_string(src):
  #detect randomized string like this; ELidMQDtIk
  randomized_string_count = 0.0
  names = []

  #extract variable
  pat = re.compile(r"\$[a-zA-Z0-9_-]+[=.:)({} ]",re.IGNORECASE)
  variables = re.findall(pat,src)

  #extract function
  pat = re.compile(r"function [a-zA-Z0-9_-]+[{ (]",re.IGNORECASE)
  functions = re.findall(pat,src)

  for name in variables:
    #create list of variables
    variable = name[:-1].strip()
    names.append(variable[1:].lower())

  for name in functions:
    #create list of functions
    function = name[:-1].strip()
    names.append(function[8:].strip().lower())
  names = list(set(names))

  for name in names:
    if len(name) < 5:
      continue
    if( 0.3 > vowel_rate(name)):
      randomized_string_count += 1
  
  
  length = len(names)
  if(length <= 10):
    return 0

  if(randomized_string_count / length < 0.45):
    return 0
  return randomized_string_count / length
  