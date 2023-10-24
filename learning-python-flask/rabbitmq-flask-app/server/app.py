import json
import pika
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"

@app.route("/contactform", methods=["POST"])
def contactform():
    # Validate the request form data

    # Convert the request form data to JSON
    json_data = json.dumps(request.form.to_dict(flat=False))

    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

        # Create a channel
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue="task_queue", durable=True)

        # Publish the message to the queue
        channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=json_data,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        # Close the connection
        connection.close()

    except pika.exceptions.AMQPConnectionError as exc:
        # Handle connection error
        print(f"Failed to connect to RabbitMQ service. Message won't be sent. {exc}")
        return None

    # Return a success message
    return f"___ Sent: {json_data}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

