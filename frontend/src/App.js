import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
    const [user, setUser] = useState('');
    const [content, setContent] = useState('');
    const [messages, setMessages] = useState([]);

    const fetchMessages = async () => {
        const apiUrl = process.env.REACT_APP_API_URL;
        const result = await axios.get(`${apiUrl}/messages`);
        setMessages(result.data);
    };

    const sendMessage = async () => {
        await axios.post('http://localhost:8000/message', {
            user,
            content
        });
        setContent('');
        fetchMessages();
    };

    useEffect(() => {
        const savedUser = localStorage.getItem('user');
        if (savedUser) {
            setUser(savedUser);
        }

        fetchMessages();

        const interval = setInterval(() => {
            fetchMessages();
        }, 2000);

        return () => clearInterval(interval);
    }, []);

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
                        <div style={{ fontSize: '0.8em', color: '#888' }}>
                            {msg.createdAt
                                ? `${msg.createdAt.slice(8, 10)}.${msg.createdAt.slice(5, 7)}.${msg.createdAt.slice(0, 4)} ${msg.createdAt.slice(11, 16)}`
                                : ''}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default App;
