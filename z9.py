import os.path
import xml.etree.ElementTree as ET
import json
from detection import extract_url, detect_sign, detect_iex, detect_strings_blacklist, detect_randomized_string,logistic_reg
from preprocess import source_context
import argparse
import datetime
import webbrowser
import re


DEBUG=False

class Z9:
  def __init__(self,sources):
    self.sources = sources
    self.report = []
    self.source_context = source_context.SourceContext()
    self.engines = []
    self.engines.append(detect_iex.DetectIEX(weight=100))
    self.engines.append(extract_url.ExtractURL(weight=20))
    self.engines.append(detect_sign.DetectSign(weight=250))
    self.engines.append(logistic_reg.LogisticReg(weight=100))
    self.engines.append(detect_randomized_string.DetectRandomizedString(weight=400))
    self.engines.append(detect_strings_blacklist.DetectStringsBlacklist(weight=1))
    
  def run_detection(self):
    
    for source in self.sources:
      self.source_context.preprocess(source["sourcecode"])
      all_results = {}
      all_results["eventrecid"] = source['eventrecid']
      all_results["time"] = source['time']
      all_results["totalscore"] = {}
      all_results["sourcecode"] = self.source_context.source
      all_results["removed_backtick"] = self.source_context.removed_backtick

      scores = {}
      total_score = 0
      results = {}
      errors = {}

      for engine in self.engines:

        engine.init()

        engine.run_detection(self.source_context)

        scores[engine.name] = engine.get_score()
        total_score += engine.get_score()
        results[engine.name] = engine.get_result()
        error = engine.get_error()
        if error:
          errors[engine.name] = error


      all_results["totalscore"]["totalscore"] = total_score
      all_results["totalscore"]["score"] = scores
      all_results["error"] = errors
      all_results.update(results)

      self.report.append(all_results)


  def json_dump(self,jsonfilename=""):
    with open(jsonfilename,'w') as f:
      json.dump(self.report,f)
    



      



def z9_dynamic(xmlfilename, jsonfilename=""):
  #Extract Sourcecode from XML
  try:
    sources=get_eventlog(xmlfilename)
  except Exception as e:
    print(f"xml parse error :{str(e)}")
    if jsonfilename!='':
      with open(jsonfilename,'w') as f:
        report = []
        report.append({"error" : f"xml parse error :{str(e)}"})
        json.dump(report,f)
    return False

  z9 = Z9(sources)
  z9.run_detection()
  if jsonfilename!='':
    z9.json_dump(jsonfilename)

def z9_static(sourcefile,jsonfilename="",encoding="utf-16"):
  #Read script from script file
  try:
    source = get_script(sourcefile,encoding)
  except Exception as e:
    print(f"Failed to open the file :{str(e)}")
    if jsonfilename!='':
      with open(jsonfilename,'w') as f:
        report = []
        report.append({"error" : f"Failed to open the file :{str(e)}"})
        json.dump(report,f)
    return False
  sourcecode = {}
  sourcecode["sourcecode"] = source
  sourcecode["time"] = {"SystemTime" : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f000Z%Z')}
  sourcecode["eventrecid"] = 0
  z9 = Z9([sourcecode])
  z9.run_detection()
  if jsonfilename!='':
    z9.json_dump(jsonfilename)


def get_script(sourcefile,encoding):
  if os.path.isfile(sourcefile):
    try:
        with open(sourcefile,"r",encoding=encoding) as f:
            sourcecode = f.read()
    except:
      raise 
    return sourcecode
  else:
    raise Exception("file not found")

def get_eventlog(filename):
  if not os.path.isfile(filename):
    print('Not found:%s' % filename)
    raise FileNotFoundError("file not found")
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

def open_viewer_html(viewer, jsonfilename):
    if not (os.path.isfile(viewer) and os.path.isfile(jsonfilename)):
        print("File not found")
        exit(1)

    try:
        with open(viewer, "r") as f_html, open(jsonfilename, "r") as f_json:
            html = f_html.read()
            json_data = f_json.read()

            textarea_pattern = r'(<textarea[^>]*id="alert_data"[^>]*>)([\s\S]*?)(<\/textarea>)'
            match = re.search(textarea_pattern, html, re.IGNORECASE)
            if match:
                
                start_tag = match.group(1)
                end_tag = match.group(3)
                
                replacement = f'{start_tag}{json_data}{end_tag}'
                replaced_html = html.replace(match.group(0), replacement)

                with open(os.path.splitext(jsonfilename)[0] + ".html","w") as new_viewer:
                    new_viewer.write(replaced_html)
                    webbrowser.open_new(new_viewer.name)


    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
  print('''
 ______                                          ___  
|__   / ____ ____ ____ ____ ____ ____ ____ ____ / _ \ 
  /  / |_  /|_  /|_  /|_  /|_  /|_  /|_  /|_  /| (_) |
 /  /_. / /  / /  / /  / /  / /  / /  / /  / /  \__. |
/_____|/___|/___|/___|/___|/___|/___|/___|/___|   /_/ 
''')
  parser = argparse.ArgumentParser()
  parser.add_argument("input", help="Input file path")
  parser.add_argument("--output", "-o", help="Output file path", default="output.json")
  parser.add_argument("-s", "--static", help="Enable Static Analysis mode", action="store_true")
  parser.add_argument("--no-viewer", help="Disable opening the JSON viewer in a web browser", action="store_true")
  
  parser.add_argument("--utf8", help="Read scriptfile in utf-8 (deprecated)", action="store_true")
  args = parser.parse_args()

  if args.static:
      print("Called static")
      z9_static(args.input, args.output, "utf-8" if args.utf8 else "utf-16")
  else:
      if args.utf8:
          print("Warning: --utf8 option is only valid with -s option.")
          exit()
      print("Called dynamic")
      z9_dynamic(args.input, args.output)

  if not args.no_viewer:
    try:
      open_viewer_html("./viewer.html",args.output)
    except Exception as e:
       print(str(e))
