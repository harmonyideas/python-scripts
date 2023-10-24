import pika


def main():
    try:
        # Connect to RabbitMQ
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue="task_queue", durable=True)

        # Start consuming messages from the queue
        channel.basic_consume(queue="task_queue", on_message_callback=callback)
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as exc:
        # Handle connection error
        print(f"Failed to connect to RabbitMQ service. Cause: {exc}")
        return

    # Wait for the consumer to be stopped
    while channel.is_consuming():
        channel.wait()


def callback(ch, method, properties, body):
    # Process the message
    print(f"Received {body.decode()}")
    print("Done")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    main()
