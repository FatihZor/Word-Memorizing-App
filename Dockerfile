# syntax=docker/dockerfile:1.4

FROM python:3.9
EXPOSE 5000
COPY ./ /app 
WORKDIR /app 
RUN python3 -m pip install -r requirements.txt --no-cache-dir
