#!/bin/bash

set -e

if [[ $1 == "clean" ]]; then
    rm -rf ./src/build
    rm -rf ./src/venv
fi

PY="python3"
PIP="pip3"

if [[ $1 != "" ]]; then
    PY="$1"
fi

if [[ $2 != "" ]]; then
    PIP="$2"
fi

rm -rf ./src/build
rm -rf ./src/venv

cd src/
mkdir build/assets/ -p
cd build/
cp ../assets/* ./assets/
cd ..

$PY -m venv venv
source venv/bin/activate

$PIP install -r ../requirements.txt

$PY -m nuitka main.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --enable-plugins=tk-inter # --follow-imports --disable-console

deactivate
rm -rf venv

mv build/main.bin build/JK_PasswordManager

echo "Compiling finished!"

