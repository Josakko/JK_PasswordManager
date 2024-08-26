#!/bin/bash

cd ../../
docker run --rm -i -v $PWD:/work -w /work/packaging/windows/offline amake/innosetup installer.iss
