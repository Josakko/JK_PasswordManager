#!/bin/bash

cd ../../
docker run --rm -i -v $PWD:/work -w /work/packaging/windows amake/innosetup installer.iss
cd packaging/windows
