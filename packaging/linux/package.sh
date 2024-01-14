#!/bin/bash

# ARCH=x86_64 appimagetool JK_PasswordManager.AppDir

cp ../src/build/JK_PasswordManager ./packaging/linux/JK_PasswordManager/usr/share/JK_PasswordManager
dpkg --build ./linux/JK_PasswordManager
mv ./linux/JK_PasswordManager.deb ../../bin/JK_PasswordManager.deb
