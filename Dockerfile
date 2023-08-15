FROM cgr.dev/chainguard/python:latest-dev as builder
USER root

WORKDIR /app

COPY requirements.txt .
COPY src/setup.py .
COPY src/masterkey_system_generator ./masterkey_system_generator

RUN pip install -r requirements.txt --user
RUN ls
RUN pip install . --user

EXPOSE 8000:8000

ENTRYPOINT [ "python", "/app/masterkey_system_generator" ]
