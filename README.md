# z9 PowerShell Log Analyzer

[Japanese](./README_ja.md)

![Z9 Logo](./img/logo.png)

## Abstract
This tools detects the artifact of the PowerShell based malware from the eventlog of PowerShell logging.

## Online Demo
[https://z9.shino.club/](https://z9.shino.club/)
* including Sandbox

## Install
```
git clone https://github.com/Sh1n0g1/z9
```

## How to use
```
python z9.py <XMLfile>
python z9.py <XMLfile> <output JSONfile>
```
The JSON file can be visualized by `viewer.html`.

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


