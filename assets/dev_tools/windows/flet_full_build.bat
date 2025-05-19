@echo off
cd /d "%~dp0..\..\.."

:: Clean previous builds
hatch run scripts:clean

:: Create dev environment
hatch env create dev

:: Pack the application
hatch run flet pack "%CD%\src\tempo_gui\__main__.py" --hidden-import=textual.widgets._tab --name tempo_gui

:: Set source and destination paths (NO spaces around '=')
set "before_file=%CD%\dist\tempo_gui.exe"
set "after_file=%CD%\assets\base\tempo_gui.exe"

:: Copy the packed executable
copy "%before_file%" "%after_file%"

:: Call the newly copied executable
call "%after_file%" --use_browser

exit /b
