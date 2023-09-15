#!/bin/bash


cd src/

mkdir build/
cd build/
mkdir assets/
cp ../assets/JK.ico assets/JK.ico
cp ../assets/loading.png assets/loading.png
cd ..


python ~/.local/lib/python3.10/site-packages/nuitka/__main__.py main.py --clang --onefile  --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build

echo "Compiling finished!"
read

