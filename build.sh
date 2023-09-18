#!/bin/bash


cd src/ || exit

mkdir build/
cd build/ || exit
mkdir assets/
cp ../assets/JK.ico assets/JK.ico
cp ../assets/loading.png assets/loading.png
cd ..


python3 ~/.local/lib/python3.10/site-packages/nuitka/__main__.py main.py --clang --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build  --onefile --standalone


echo "Compiling finished!"

