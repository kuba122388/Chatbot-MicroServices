import os
import pika
import json
import time
import sys

# Połączenie z RabbitMQ
def connect_to_rabbitmq():
    while True:
        try:
            print("Trying to connect to RabbitMQ...", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
            channel = connection.channel()
            channel.queue_declare(queue='chatbot_queue')
            print("Successfully connected to RabbitMQ.", flush=True)
            return channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}", flush=True)
            print("Retrying in 10 seconds...", flush=True)
            time.sleep(10)

# Obsługa wiadomości z kolejki
def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Received message: {message}", flush=True)
        user_message = message.get('content', '[no content]')
        print(f"User message: {user_message}", flush=True)
    except Exception as e:
        print(f"Failed to process message: {e}", flush=True)
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Worker - start
def start_worker():
    channel = connect_to_rabbitmq()
    channel.basic_consume(queue='chatbot_queue', on_message_callback=on_message)
    print("Waiting for messages. To exit press CTRL+C\n", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
