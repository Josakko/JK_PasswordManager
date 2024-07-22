#!/bin/bash

set -e

cd ../../

docker build -t jkpm/nuitka-image -f building/linux/Dockerfile .
# docker run --rm jkpm/nuitka-image
# docker run --rm -v $(pwd)/output:/output jkpm/nuitka-image sh -c "cp /path/to/your/binary /output/binary_name"

# docker run jkpm/nuitka-image sh -c "pwd && cd /app/src && python -m nuitka main.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --enable-plugins=tk-inter " 

docker run --rm -i -v $PWD/out:/app/out -w /app/out jkpm/nuitka-image sh -c "cd /app/src && python -m nuitka main.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --enable-plugins=tk-inter && cp /app/src/build/main.bin /app/out/main.bin" # --follow-imports --disable-console

# docker cp jkpm/nuitka-image:/app/src/build/main.bin ./main.bin
