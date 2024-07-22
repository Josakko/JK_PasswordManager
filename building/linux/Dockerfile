FROM python:3.11.9-bullseye

WORKDIR /app

RUN apt update
RUN apt install patchelf clang -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir src
COPY src/ src/

RUN ls
RUN cd src
RUN ls
RUN cd src && ls

# RUN cd src && python -m nuitka main.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --enable-plugins=tk-inter 
# --follow-imports --disable-console

# RUN cp src/build/main.bin /work/out/main.bin
# COPY src/build/main.bin /main.bin
