import os
import json
import pika
import time
import sys
from datetime import datetime
from pymongo import MongoClient
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Połączenie z MongoDB
client = MongoClient("mongodb://root:example@mongo:27017")
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

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue'))
            channel = connection.channel()
            channel.queue_declare(queue='chatbot_queue')

            print("✅ Connected to RabbitMQ.")
            sys.stdout.flush()

            return channel
        except Exception as e:
            print(f"❌ RabbitMQ error: {e}")
            print("Retrying in 10 seconds...")
            sys.stdout.flush()
            time.sleep(10)

# Obsługa wiadomości z kolejki
def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        user_message = message.get('content', '[no content]')

        print(f"📩 User message: {user_message}")
        sys.stdout.flush()

        # 🧠 Odpowiedź z Gemini
        response = model.generate_content(user_message)
        bot_response = response.text.strip()

        print(f"🤖 Gemini: {bot_response}")
        sys.stdout.flush()

        bot_message = {
            "user": "bot",
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
    print("📋 Dostępne modele:")
    for m in genai.list_models():
        print(f"- {m.name} ({'✅' if 'generateContent' in m.supported_generation_methods else '❌'})")

    channel = connect_to_rabbitmq()
    channel.basic_consume(queue='chatbot_queue', on_message_callback=on_message)
    print("🟢 Waiting for messages...")
    sys.stdout.flush()
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
