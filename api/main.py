from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

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

messages = []

@app.get("/messages", response_model=List[Message])
async def get_messages():
    return messages

@app.post("/message")
async def post_message(message: Message):
    messages.append(message)
    return {"status": "ok"}