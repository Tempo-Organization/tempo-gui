@echo on

cd /d "%~dp0"

cd /d "..\..\.."

set "after_file=%CD%\assets\base\tempo_gui.exe"

if exist "%after_file%" (call "%after_file%")

exit /b
