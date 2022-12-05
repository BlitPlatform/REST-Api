FROM ubuntu:18.04
FROM continuumio/miniconda3
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt-get update && \
      apt-get -y --no-install-recommends install sudo && \
      apt-get -y install freecad

WORKDIR /app
#WORKDIR .

# Create the environment:
COPY blitenvironment.yml .
RUN conda env create -f blitenvironment.yml

# Activate the environment, and make sure it's activated:
SHELL ["conda", "run", "-n", "blitairest", "/bin/bash", "-c"]
#RUN conda activate blitairest
RUN python -c "import pytest"
RUN python -c "from fastapi import FastAPI"

COPY . /app

EXPOSE 8000

WORKDIR /app


CMD uvicorn --host=0.0.0.0 main:app
#RUN ["chmod", "+x", "/app/startup.sh"]
#ENTRYPOINT ["/app/startup.sh"]
