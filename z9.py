import sys
import os.path
import xml.etree.ElementTree as ET
import json
from detection import extract_url, detect_sign, detect_iex, detect_strings_blacklist, detect_randomized_string,logistic_reg
import score
import raise_alert
import remove_backtick


DEBUG=False

def main(xmlfilename, jsonfilename=""):
  #Extract Sourcecode from XML
  sources=get_eventlog(xmlfilename)
  
  alert_data=[]
  for source in sources:
    
    sourcecode=source['sourcecode']
    time=source['time']
    eventrecid=source['eventrecid']
    
    #preprocessing
    removed_backtick=remove_backtick.remove_backtick(sourcecode)
    #detection engines
    detect_iex_result=detect_iex.detect_iex(removed_backtick) #True or False
    url_result=extract_url.extract_url(removed_backtick)
    detect_sign_result=detect_sign.detect_sign(sourcecode)
    detect_randomized_string_result=detect_randomized_string.detect_randomized_string(sourcecode)
    detect_strings_blacklist_result=detect_strings_blacklist.detect_strings_blacklist(removed_backtick)
    logistic_reg_result = logistic_reg.logistic_reg(removed_backtick)
    
    all_results={
      "detect_iex":detect_iex_result,
      "extract_url":url_result,
      "detect_sign":detect_sign_result,
      "unreadable_string":detect_randomized_string_result,
      "detect_strings_blacklist":detect_strings_blacklist_result,
      "logistic_reg":logistic_reg_result
    }
    totalscore=score.score(all_results)
    if DEBUG or totalscore["totalscore"] >=100:
      raise_alert.raise_alert(time, sourcecode, url_result, totalscore)

    if DEBUG:
      input()
    #Prepare JSON DATA
    if jsonfilename!='':
      alert_data.append({
        "eventrecid":eventrecid,
        "time":time,
        "totalscore":totalscore,
        "sourcecode":sourcecode,
        "removed_backtick":removed_backtick,
        "detect_iex":detect_iex_result,
        "url_result":url_result,
         "detect_sign":detect_sign_result,
        "unreadable_string":detect_randomized_string_result,
        "detect_strings_blacklist":detect_strings_blacklist_result,
        "logistic_reg":logistic_reg_result,
      })
  if jsonfilename!='':
    #Create JSON file
    with open(jsonfilename,'w') as f:
      json.dump(alert_data,f)
      

def get_eventlog(filename):
  if not os.path.isfile(filename):
    print('Not found:%s' % filename)
    exit(1)
  ns='{http://schemas.microsoft.com/win/2004/08/events/event}'  #namespace
  f = open(filename, 'r', encoding='utf-16')
  xml=f.read()
  xml= "<eventlog>" + xml + "</eventlog>"
  root = ET.fromstring(xml)
  sources=[]
  for event in root:
    for e in event:
      for f in e:
        pass
    eventid=event.find(ns + 'System').find(ns + 'EventID').text
    eventrecid=event.find(ns + 'System').find(ns + 'EventRecordID').text
    time=event.find(ns + 'System').find(ns + 'TimeCreated').attrib
    ps=event.find(ns + 'EventData').findall(ns + 'Data')
    if eventid=="4104" or eventid=="4103":
      if(ps[2].text):
        sources.append({"sourcecode":ps[2].text, "time":time, "eventrecid": eventrecid})
    elif eventid=="800":
      if(ps[0].text):
        sources.append({"sourcecode":ps[0].text, "time":time, "eventrecid": eventrecid})
  return sources

if __name__ == '__main__':
  print('''
 ______                                          ___  
|__   / ____ ____ ____ ____ ____ ____ ____ ____ / _ \ 
  /  / |_  /|_  /|_  /|_  /|_  /|_  /|_  /|_  /| (_) |
 /  /_. / /  / /  / /  / /  / /  / /  / /  / /  \__. |
/_____|/___|/___|/___|/___|/___|/___|/___|/___|   /_/ 
''')
  if(len(sys.argv) < 2):
    print("Usage: python z9.py <xml filepath>\n")
    print("Usage: python z9.py <xml filepath> <output json filename>\n")
    print("Example: python z9.py .\\util\\log\\mwpsop.xml result.json")
    exit()
  elif(len(sys.argv)==2):
    xmlfilename=sys.argv[1]
    main(xmlfilename)
  elif(len(sys.argv)==3):
    xmlfilename=sys.argv[1]
    jsonfilename=sys.argv[2]
    main(xmlfilename, jsonfilename)
  main(sys.argv[1])
  
