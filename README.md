# 🤖 Chatbot with Gemini + FastAPI + React + RabbitMQ + MongoDB

This is a simple chatbot app with a React frontend and Python backend, using Google Gemini for AI responses. Messages are passed via RabbitMQ and stored in MongoDB.

---

## 🧰 Stack

- **Frontend**: React + Axios
- **Backend API**: FastAPI + MongoDB + RabbitMQ (as producer)
- **Worker**: Python + Google Generative AI (Gemini) + RabbitMQ (as consumer)
- **Database**: MongoDB
- **Queue**: RabbitMQ with management UI

---

## ⚙️ Features

- Real-time chatbot messages
- Message history stored in MongoDB
- Text formatting support (`**bold**`, `_italic_`)
- Auto-replies using Gemini
- Periodic message refresh (every 2s)
- Clear message history button
- Asynchronous message processing with RabbitMQ (message queue for communication between services)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Set environment variables

#### 📁 Create a ```.env``` file in the root directory:

```
MONGO_URI=mongodb://root:example@mongo:27017/
RABBITMQ_HOST=queue
CHATBOT_QUEUE=chatbot_queue
GEMINI_API_KEY=your_google_gemini_api_key
REACT_APP_API_URL=http://localhost:8000
```

#### 📁 Create a file called ```.env.local``` inside the frontend/ directory:

```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Run the app using Docker Compose
```
docker-compose up --build
```
#### This will start:
- FastAPI on http://localhost:8000
- Frontend on http://localhost:3000
- RabbitMQ UI on http://localhost:15672 (default: guest/guest)
- Mongo Express on http://localhost:8081

---

### 🧪 Example Usage 
#### 1. Open http://localhost:3000
#### 2. Enter your name and a message
#### 3. Submit it – Gemini will auto-respond after a short delay

Click “Clear all messages” to delete history

---

### 📁 Project Structure
```bash
.
├── api/          # FastAPI backend
├── chatbot/      # Worker using Gemini + RabbitMQ
├── frontend/     # React frontend
├── docker-compose.yml
└── .env          # Environment config
```

---

### ✅ Requirements
- Docker & Docker Compose
- Google API Key with access to Gemini

---

### 📌 Notes
1. Messages are sent to RabbitMQ by the API and consumed by the chatbot worker.
2. Gemini replies are inserted back into MongoDB.
3. Frontend polls messages every 2 seconds, but this can later be upgraded to WebSockets for real-time communication.
4. The backend (FastAPI) and worker (Gemini) are containerized using Docker, and all services are orchestrated with Docker Compose.
5. Ensure to update your .env file with the correct MongoDB URI, RabbitMQ host, and Google Gemini API key.

---

