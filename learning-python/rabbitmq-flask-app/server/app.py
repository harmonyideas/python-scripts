from flask import Flask, request
import pika, json

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/contactform', methods=['POST'])
def contactform():
    json_data = json.dumps(request.form.to_dict(flat=False))
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json_data,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    connection.close()
    return " ___ Sent: %s" % json_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
