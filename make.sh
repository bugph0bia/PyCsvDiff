#!/bin/bash

# activate venv
python3 -m venv .venv-linux
. .venv-linux/bin/activate

# install pyinstaller
pip3 install pyinstaller

# make work directory
mkdir pyinstaller-linux
cd pyinstaller-linux

# run pyinstaller
pyinstaller ../csvdiff.py --onefile

# copy binary
cd ..
mkdir bin
cp pyinstaller-linux/dist/csvdiff bin/

# finish
deactivate
rm -rf .venv-linux
rm -rf pyinstaller-linux
