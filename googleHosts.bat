Net session >nul 2>&1 || mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0","","runas",1)(window.close)&&exit
set url=google.cn
set hosts=%SystemRoot%\system32\drivers\etc\hosts
for /f "delims= " %%i in ('ping %url% -n 1 ^|findstr "^[0-9]"') do (
findstr %%i %hosts% || (
more %hosts% > hosts.history
echo %%i translate.googleapis.com > %hosts%
echo.%%i translate.google.com >> %hosts%
echo.
more hosts.history >> %hosts%
)
ipconfig/flushdns
)
exit