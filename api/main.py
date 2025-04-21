from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
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

class MessageOut(Message):
    createdAt: Optional[str]

def send_to_queue(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='queue')
    )
    channel = connection.channel()

    channel.queue_declare(queue='chatbot_queue')

    body = json.dumps(message)

    channel.basic_publish(exchange='',
                          routing_key='chatbot_queue',
                          body=body)

    print(f"[x] Wysłano do kolejki: {body}")
    connection.close()

@app.get("/messages", response_model=List[MessageOut])
async def get_messages():
    messages_cursor = messages_collection.find().sort([('createdAt', -1)])
    messages_list = list(messages_cursor)

    return [{
        "user": msg["user"],
        "content": msg["content"],
        "createdAt": msg.get("createdAt")
    } for msg in messages_list]


@app.post("/message")
async def post_message(message: Message):
    message_dict = message.dict()
    message_dict['createdAt'] = datetime.now().isoformat()

    messages_collection.insert_one(message_dict)

    message_dict.pop("_id", None)
    send_to_queue(message_dict)

    return {"status": "ok"}