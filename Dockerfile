# Test Support Container

FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get upgrade && apt-get update
RUN apt install vim -y
RUN apt install curl -y

ENTRYPOINT ["tail", "-f", "/dev/null"]
