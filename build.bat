@echo off


cd src\

mkdir build\assets\
copy assets build\assets\

:: --windows-icon-from-ico=assets\JK.ico

nuitka main.py --clang --onefile  --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build 

echo Compiling finished!
pause