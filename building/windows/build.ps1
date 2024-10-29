Remove-Item .\src\build
Remove-Item .\src\venv

Set-Location src\

python -m venv venv

venv\Scripts\activate

mkdir build\assets\
Copy-Item assets build\assets\

pip install -r ..\requirements.txt

python -m nuitka main.py --clang --onefile  --enable-plugins=tk-inter --standalone --windows-console-mode=disable --clean-cache=all --remove-output --output-dir=..\out\windows-out --output-filename=JK_PasswordManager.exe --windows-icon-from-ico=assets\icon.png --prefer-source-code # --follow-imports

Write-Output "Compiling finished!"
pause

