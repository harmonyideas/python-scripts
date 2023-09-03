FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev celery curl

COPY requirements.txt /app/requirements.txt
COPY start_app.sh /app/start_app.sh

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

EXPOSE 8982

RUN ["chmod", "+x", "/app/start_app.sh"]
ENTRYPOINT ["/app/start_app.sh"]
