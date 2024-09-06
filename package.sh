#!/bin/bash

set -e

if [[ -d ./src/ ]]; then
    :

elif [[ -d ./linux/ && -d ./windows/ ]]; then
    cd ..

else
    echo "[!] Working directory must be in the root direcotry or in the packaging directory!"
    exit
fi

VERPATH="./version"
version="$1"

clean() {
    echo "[!] Cleaning the repo directory"

    echo "[+] Removing output folders"
    while IFS= read -r line; do
        echo "[log] Deleting ./out/$line"
        sudo rm -rf "./out/$line"
    done < "./out/.gitignore"

    echo "[log] Removing windows packaging outputs"
    rm -rf ./packaging/windows/offline/Output
    rm -rf ./packaging/windows/web/Output

    echo "[+] Finished cleaning packaging direcotry"
}


if [[ "$version" == "clean" ]]; then
    clean
    exit
fi


if [[ "$version" != "" ]]; then
    echo "$version" > "$VERPATH"
    echo "Setting version: $version"

else
    version="$(cat "$VERPATH")"
    echo "Using version: $version"

fi 

echo "[log] Compiling for linux"
cd ./building/linux/
./build.sh
cd ../../
echo "[+] Finished compiling for linux"

echo "[log] Packaging deb"
cp ./out/linux-out/main.bin ./packaging/linux/JK_PasswordManager/usr/share/jkpm-inst/jkpm
cd ./packaging/linux
./package.sh
cd ../../
echo "[+] Finished packaging deb"

echo "[log] Building windows web installer"
cd ./packaging/windows
./package-web.sh
cd ../../
echo "[+] Finished building web installer for windows"

if [[ -f ./out/windows-out/JK_PasswordManager.exe ]]; then
    echo "[log] Packaging windows offline installer since windows executable is present"
    cd ./packaging/windows
    ./package-offline.sh
    cd ../../
    echo "[+] Finished building windows offline installer"

else
    echo "[-] Skiping building offline windows installer since executable is not present"
fi


# TODO: contenerize compiling for windows (if "practically" possible)
