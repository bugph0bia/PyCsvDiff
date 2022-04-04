@echo off

rem activate venv
python -m venv .venv-win
call .venv-win\Scripts\activate

rem install pyinstaller
pip install pyinstaller

rem make work directory
mkdir pyinstaller-win
cd pyinstaller-win

rem run pyinstaller
pyinstaller ../csvdiff.py --onefile

rem copy binary
cd ..
mkdir bin
copy pyinstaller-win\dist\csvdiff.exe bin\

rem finish
call deactivate
rmdir /s /q .venv-win
rmdir /s /q pyinstaller-win
