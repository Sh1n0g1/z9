cd %~dp0

wevtutil query-events "Windows Powershell" /uni:true /f:XML > log\winps.xml
wevtutil query-events Microsoft-Windows-PowerShell/Operational /uni:true /f:XML > log\mwpsop.xml