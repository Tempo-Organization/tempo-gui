@echo on

cd /d "%~dp0"

call install_hatch.bat

cd /d "..\..\.."

set "dist_dir=%CD%\dist"

if exist "%dist_dir%" (rmdir /s /q "%dist_dir%")

set "build_dir=%CD%\build"

if exist "%build_dir%" (rmdir /s /q "%build_dir%")

hatch run flet pack "%CD%\src\tempo_gui\__main__.py" --name tempo_gui

set "before_file=%dist_dir%\tempo_gui.exe"

set "after_file=%CD%\assets\base\tempo_gui.exe"

if exist "%before_file%" (copy /Y "%before_file%" "%after_file%")

if exist "%after_file%" (call "%after_file%")

exit /b
