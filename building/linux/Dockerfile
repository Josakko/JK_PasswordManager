FROM python:3.11.9-bullseye

WORKDIR /app
SHELL ["/bin/bash", "-c"]

RUN apt update && apt install apt-utils patchelf clang -y

RUN mkdir src
COPY src/ src/

COPY requirements.txt requirements.txt

RUN cd src && \
    python -m venv venv && \
    source venv/bin/activate && \
    python -m pip install --upgrade pip && \
    pip install -r ../requirements.txt

