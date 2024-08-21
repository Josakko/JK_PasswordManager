#!/bin/bash

set -e
cd ../../
version="$(cat ./version)"

docker build -t jkpm/jkpm-linux-deb -f ./packaging/linux/Dockerfile .

docker run --rm -i -v $PWD/out/deb-out:/work/out -w /work/out jkpm/jkpm-linux-deb dpkg-deb --build /work/jkpm /work/out/jkpm-$version.deb

