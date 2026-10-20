import json
import pika
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"

@app.route("/contactform", methods=["POST"])
def contactform():
    # Validate the request form data

    # Convert the request form data to JSON
    form_data = request.form.to_dict(flat=False)
    json_data = json.dumps(form_data)

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
        return jsonify({"status": "error", "message": "Message queue unavailable"}), 503

    # Return a success message as JSON. jsonify sets application/json and escapes
    # the user-supplied values, so they are not reflected as HTML.
    return jsonify({"status": "sent", "data": form_data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")

