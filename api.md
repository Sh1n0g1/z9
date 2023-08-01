
# Z9 API

Z9 determine if source code written in PowerShell scripts is malware.


## 1. Upload File

### Endpoint : 

```
https://z9.shino.club/_upload_sourcecode.php
```

### POST Parameters : 
| Key         | Outline                                                        |
| ----------- | -------------------------------------------------------------- |
| sourcecode  | Content of the file. The upload file must be an executable file written in PowerShell. |

### Response :

| Key        | Outline                                                    |
| ---------- | ---------------------------------------------------------- |
| result     | If this is true, the POST request is successful.                  |
| filename   | This is the filename. It will be used by `https://z9.shino.club/_get_file_status.php` and `https://z9.shino.club/_upload_sourcecode.php`. |

<!-- 
```zsh 
{"result":bool,"filename": string,"sandboxstatus":{"qemu_status":string,"output":["shinogi  2850063  0.0  0.0   2888   988 ?        S    09:12   0:00 sh -c ps -aux | grep qemu","shinogi  2850065  0.0  0.0   3468  1624 ?        S    09:12   0:00 grep qemu"],"count":int}} 
```
-->

### Example : 
```zsh
$ curl -X POST -d "sourcecode="@${filename} https://z9.shino.club/_upload_sourcecode.php
```

## 2. Get Sandbox Status

### Endpoint : 

```
https://z9.shino.club/_get_file_status.php
```
### GET parameter : 

|  key  |  outline  |
| ---- | ---- |
|  file  |    `filename` from  [1. Upload File](#1-upload-file) `https://z9.shino.club/_upload_sourcecode.php`. |


### Response :
|  key  |  outline  |
| ---- | ---- |
|  result  |  If this is `true`, your uploaded file is accepted. |
|  status  |  This value takes `done` or `queue`. When it is `queue`, Z9 is waiting for processing in sandbox.   |
|  count  |  Your number on the queue.  |
|  total  |  The number of waiting list.  |
|  error  |  Error message.  |


### Example : 
```zsh
$ curl 'https://z9.shino.club/_get_file_status.php?file={filename}'
```


## 3. Get Result
You can get the result URL when the status is `done`.

### Endpoint : 
```
https://z9.shino.club/result.php
```

### GET parameter : 

|  key  |  outline  |
| ---- | ---- |
|  file  |    `filename` from  [1. Upload File](#1-upload-file) `https://z9.shino.club/_upload_sourcecode.php`. |


### Response : 
You can get a HTML file with the JSON result in it.

### Example : 
```zsh
$ curl 'https://z9.shino.club/result.php?file={filename}' > result.html
```

## Example for making use of Z9 API with Python


```python
import requests
import json
from chardet.universaldetector import UniversalDetector
import time
import os
import json
import sys
from bs4 import BeautifulSoup

def uploadFile(URL="https://z9.shino.club/_upload_sourcecode.php", FILENAME=""):

  # Check file capacity
  path=FILENAME
  file_size = os.path.getsize(path)
  print("file capacity is", file_size, "bytes")

  # Write the contents of the file you want to examine
  sourcecode = ""
  with open(FILENAME, "r", encoding=getEncoding(FILENAME)) as f:
    for line in f:
      sourcecode += line

  response = requests.post(url=URL, data={"sourcecode" : sourcecode})

  # Get the URL of the result
  return "https://z9.shino.club/result.php?file=" + response.json()["filename"]

def getEncoding(path):

  with open(path, 'rb') as f:
    detector = UniversalDetector()
    for line in f:
      detector.feed(line)
      if detector.done:
        break
    detector.close()
    result = detector.result
    return result["encoding"]


def getStatus(filename, URL="https://z9.shino.club/_get_file_status.php"):
    URL += "?file=" + filename
    res = requests.get(URL)
    print(res)
    return res

def getJson(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    result_file = open("result.json", 'w')
    result_file.write(soup.findAll('textarea')[0].text[1:-1])
    result_file.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage : python3 <this filename> <your file path>")
    path = sys.argv[1]
    result_url = uploadFile(FILENAME=path)
    sandbox_filename = result_url[38:]
    while True:
        time.sleep(30)
        if getStatus(sandbox_filename).json()["status"] == "done":
            # get url
            print(result_url)
            # download json file
            getJson(result_url)
            break
```

