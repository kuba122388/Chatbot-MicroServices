import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [user, setUser] = useState('');
  const [content, setContent] = useState('');
  const [messages, setMessages] = useState([]);

  const fetchMessages = async () => {
    const result = await axios.get('http://localhost:8000/messages');
    setMessages(result.data);
  };

  const sendMessage = async () => {
    await axios.post('http://localhost:8000/message', {
      user,
      content
    });
    setUser('');
    setContent('');
    fetchMessages(); // Pobieramy nowe wiadomości po dodaniu
  };

  return (
    <div>
      <h1>Chatbot</h1>
      <input
        type="text"
        placeholder="Your name"
        value={user}
        onChange={(e) => setUser(e.target.value)}
      />
      <textarea
        placeholder="Your message"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>

      <h2>Messages:</h2>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>
            <strong>{msg.user}:</strong> {msg.content}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
