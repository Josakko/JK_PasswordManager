#!/bin/bash

set -e
cd ../../

docker build -t jkpm/jkpm-linux-nbuild -f building/linux/Dockerfile .

docker run --rm -i -v $PWD/out:/app/out -w /app/src jkpm/jkpm-linux-nbuild /bin/bash -c "source venv/bin/activate && \
python -m nuitka main.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --enable-plugins=tk-inter --prefer-source-code --linux-icon=assets/icon.png && \
cp /app/src/build/main.bin /app/out/main.bin" 
# --follow-imports --disable-console
