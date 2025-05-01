import os
import json
import pika
import time
import sys
from datetime import datetime
from pymongo import MongoClient
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URL = os.getenv("MONGO_URI")
QUEUE = os.getenv("RABBITMQ_HOST")
QUEUE_NAME = os.getenv("CHATBOT_QUEUE")

genai.configure(api_key=GOOGLE_API_KEY)

# Connection with MongoDB
client = MongoClient(MONGO_URL)
db = client["mydatabase"]
messages_collection = db.messages

# Gemini model
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")

# RabbitMQ
def connect_to_rabbitmq():
    while True:
        try:
            print("🔄 Connecting to RabbitMQ...")
            sys.stdout.flush()

            connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)

            print("✅ Connected to RabbitMQ.")
            sys.stdout.flush()

            return channel
        except Exception as e:
            print(f"❌ RabbitMQ error: {e}")
            print("Retrying in 10 seconds...")
            sys.stdout.flush()
            time.sleep(10)

# Queue handler
def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        user_message = message.get('content', '[no content]')

        print(f"📩 User message: {user_message}")
        sys.stdout.flush()

        response = model.generate_content(user_message)
        bot_response = response.text.strip()

        print(f"🤖 Gemini: {bot_response}")
        sys.stdout.flush()

        bot_message = {
            "user": "Chatbot",
            "content": bot_response,
            "createdAt": datetime.now().isoformat()
        }

        messages_collection.insert_one(bot_message)

    except Exception as e:
        print(f"⚠️ Error while processing message: {e}")
        sys.stdout.flush()
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    channel = connect_to_rabbitmq()
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    print("🟢 Waiting for messages...")
    sys.stdout.flush()
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()