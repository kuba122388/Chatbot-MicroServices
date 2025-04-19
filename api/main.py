from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import pika
import json

client = MongoClient("mongodb://root:example@mongo:27017")
db = client["mydatabase"]
print(client.list_database_names())
dblist = client.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")

messages_collection = db.messages


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    user: str
    content: str

def send_to_queue(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='queue')
    )
    channel = connection.channel()

    channel.queue_declare(queue='chatbot_queue')

    # Przekształcamy wiadomość w JSON
    body = json.dumps(message)

    # Wysyłamy wiadomość
    channel.basic_publish(exchange='',
                          routing_key='chatbot_queue',
                          body=body)

    print(f"[x] Wysłano do kolejki: {body}")
    connection.close()


@app.get("/messages", response_model=List[Message])
async def get_messages():
    messages_cursor = messages_collection.find()
    messages_list = list(messages_cursor)
    return [{"user": msg["user"], "content": msg["content"]} for msg in messages_list]

@app.post("/message")
async def post_message(message: Message):
    message_dict = message.dict()
    messages_collection.insert_one(message_dict)

    message_dict.pop("_id", None)
    send_to_queue(message_dict)

    return {"status": "ok"}

