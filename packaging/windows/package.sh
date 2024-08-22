#!/bin/bash

cd ../../
docker run --rm -i -v $PWD:/work -w /work/packaging/windows/offline amake/innosetup installer.iss
docker run --rm -i -v $PWD:/work -w /work/packaging/windows/web amake/innosetup web-installer.iss
