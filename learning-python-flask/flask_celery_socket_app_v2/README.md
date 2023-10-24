# Asynchronous Tasks with Flask, Celery, socketIO, gunicorn and RabbitMQ
Upload a text file/files to get the top 10 most frequent word occurences

Code is based on this excellent example:  [example code](https://github.com/jwhelland/flask-socketio-celery-example/tree/master). 

## How to use this project?

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:8982](http://localhost:8982) to upload the txt file(s) 


