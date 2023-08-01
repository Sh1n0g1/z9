# z9 PowerShell Log Analyzer

[Japanese](./README.md)

![Z9 Logo](./img/logo.png)

## Abstract
This tools detects the artifact of the PowerShell based malware from the eventlog of PowerShell logging.

## Install
```
git clone https://github.com/Sh1n0g1/z9
```

## How to use
```
usage: z9.py [-h] [--output OUTPUT] [-s] [--no-viewer] [--utf8] input

positional arguments:
  input                 Input file path

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file path
  -s, --static          Enable Static Analysis mode
  --no-viewer           Disable opening the JSON viewer in a web browser
  --utf8                Read scriptfile in utf-8 (deprecated)
```


### Analyze Event Logs (Recommended)
```
python z9.py <input file> -o <output json>
python z9.py <input file> -o <output json> --no-viewer
```
|Arguments               |       Meaning                             |
|-------------------------|----------------------------------------|
|`input file`            |XML file exported from eventlog          |
|`-o output json`        |filename of z9 result                    |
|`--no-viewer `          |do not open the viewer                   |

Example)
```
python z9.py util\log\mwpsop.xml -o sample1.json
```

### Analyze PowerShell File Statically
* This approach will only do the static analysis and may not provide a proper result especially when the sample is obfuscated.
```
python z9.py <入力ファイル> -o <output json> -s
python z9.py <入力ファイル> -o <output json> -s --utf8
python z9.py <入力ファイル> -o <output json> -s --no-viewer
```
|Arguments               |       Meaning                             |
|-------------------------|----------------------------------------|
|`input file`            |PowerShell file to be analyzed           |
|`-o output json`        |filename of z9 result                    |
|`-s`                     |perform static analysis                      |
|`--utf8`                 |specify when the input file is in UTF-8       |
|`--no-viewer `          |do not open the viewer                   |

Example)
```
python z9.py malware.ps1 -o sample1.json -s
```

## How to prepare the XML file
### Enable PowerShell Logging
1. Right-click and merge this registry file:[`util/enable_powershell_logging.reg`](./util/enable_powershell_logging.reg) .
2. Reboot the PC
3. All powershell execution will be logged in eventlog

### Export Eventlog to XML
1. Execute this batch file:[`util/collect_psevent.bat`](./util/collect_psevent.bat) .
2. The XML files will be created under `util/log` directory.
3. Both XML file can be parsed by this tool.

### How to Delete the Existing Eventlog
* Execute this batch file:[`util/collect_psevent.bat`](./util/clear_psevent.bat) with "Run as Admin"


## Authors
[hanataro-miz](https://github.com/hanataro-miz)  
[si-tm](https://github.com/si-tm)  
[take32457](https://github.com/take32457)  
[Bigdrea6](https://github.com/Bigdrea6)  
[azaberrypi](https://github.com/azaberrypi)  
[Sh1n0g1](https://github.com/Sh1n0g1)  
