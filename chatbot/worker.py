import os
import json
import pika
import time
import sys
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

credentials_path = "dialogflow-creds.json"

credentials = service_account.Credentials.from_service_account_file(credentials_path)
project_id = "chatbot-agent-wu9l"

def detect_intent_texts(session_id, text, language_code="pl"):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

# Połączenie z RabbitMQ
def connect_to_rabbitmq():
    while True:
        try:
            print("Trying to connect to RabbitMQ...")
            sys.stdout.flush()
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
            channel = connection.channel()
            channel.queue_declare(queue='chatbot_queue')
            print("Successfully connected to RabbitMQ.")
            sys.stdout.flush()
            return channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            print("Retrying in 10 seconds...")
            sys.stdout.flush()
            time.sleep(10)

# Obsługa wiadomości z RabbitMQ
def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Received message: {message}")
        sys.stdout.flush()

        user_message = message.get('content', '[no content]')
        print(f"User message: {user_message}")
        sys.stdout.flush()

        session_id = "session"
        response = detect_intent_texts(session_id, user_message)

        print(f"Dialogflow Response: {response}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Failed to process message: {e}")
        sys.stdout.flush()
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Worker - start
def start_worker():
    channel = connect_to_rabbitmq()
    channel.basic_consume(queue='chatbot_queue', on_message_callback=on_message)
    print("Waiting for messages. To exit press CTRL+C")
    sys.stdout.flush()
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
