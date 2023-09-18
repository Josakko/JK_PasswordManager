#!/bin/bash


cd src/ || exit

mkdir build/
cd build/ || exit
mkdir assets/
cp ../assets/JK.ico assets/JK.ico
cp ../assets/loading.png assets/loading.png
cd ..

rm -rf venv
python3 -m venv venv
source venv/bin/activate

curl -o req.txt https://raw.githubusercontent.com/Josakko/JK_PasswordManager/main/requirements.txt
pip3 install -r req.txt

python3 -m nuitka main.py --clang --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build --onefile --standalone


deactivate
rm -rf venv
rm -rf req.txt

echo "Compiling finished!"

