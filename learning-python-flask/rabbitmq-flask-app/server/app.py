import json
import pika
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"

# Required form fields and the maximum length allowed for each one
CONTACT_FIELDS = {
    "firstname": 100,
    "lastname": 100,
    "country": 100,
    "subject": 5000,
}


def validate_contactform(form):
    """Return a list of validation errors. An empty list means the form is valid."""
    errors = []
    for field, max_length in CONTACT_FIELDS.items():
        values = form.getlist(field)
        if len(values) != 1:
            errors.append(f"{field} is required and must be given exactly once")
            continue
        value = values[0]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")
        elif len(value) > max_length:
            errors.append(f"{field} must be at most {max_length} characters")
    return errors


@app.route("/contactform", methods=["POST"])
def contactform():
    # Reject missing, empty, non-string or oversized fields before queuing
    errors = validate_contactform(request.form)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

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

