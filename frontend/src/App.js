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

    const clearMessages = async () => {
        const confirmed = window.confirm("Are you sure you want to delete all messages?");
        if (!confirmed) return;

        try {
            await axios.delete(`${process.env.REACT_APP_API_URL}/messages`);
            fetchMessages();
        } catch (error) {
            console.error("Failed to delete messages:", error);
        }
    };

    const sendMessage = async () => {
        if (!user || !content.trim() || user === `Chatbot`) return;

        await axios.post(`${process.env.REACT_APP_API_URL}/message`, {
            user,
            content,
        });
        setContent('');
        fetchMessages();
    };

    const formatText = (text) => {
        const formattedText = text.split(/(\*\*[^*]+\*\*|_[^_]+_)/g).map((part, index) => {
            if (part.startsWith("**") && part.endsWith("**")) {
                return <strong key={index}>{part.slice(2, -2)}</strong>;
            }
            if (part.startsWith("_") && part.endsWith("_")) {
                return <em key={index}>{part.slice(1, -1)}</em>;
            }
            return part;
        });

        return formattedText;
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
        <div style={styles.container}>
            <h1 style={styles.heading}>💬 Chatbot</h1>

            <div style={styles.inputGroup}>
                <input
                    style={styles.input}
                    type="text"
                    placeholder="Your name"
                    value={user}
                    onChange={(e) => setUser(e.target.value)}
                />
                <textarea
                    style={styles.textarea}
                    placeholder="Your message"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            sendMessage();
                        }
                    }}
                />
                <button style={styles.button} onClick={sendMessage}>Send</button>
                <div style={styles.clear}>
                    <button style={styles.button2} onClick={clearMessages}>✗ Clear all messages</button>
                </div>
            </div>

            <h2 style={{ marginTop: '30px' }}>Messages:</h2>
            <ul style={styles.messageList}>
                {messages.map((msg, index) => (
                    <li key={index} style={styles.messageItem}>
                        <strong>{msg.user === 'Chatbot' ? '🤖 ' : ''}{msg.user}:</strong>
                        <div style={styles.messageContent}>
                            {formatText(msg.content)}
                        </div>
                        <div style={styles.timestamp}>
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

const styles = {
    container: {
        maxWidth: '600px',
        margin: '40px auto',
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '12px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#fafafa',
    },
    heading: {
        textAlign: 'center',
        color: '#333',
    },
    inputGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        marginBottom: '20px',
    },
    input: {
        padding: '10px',
        borderRadius: '6px',
        border: '1px solid #ccc',
        fontSize: '16px',
    },
    textarea: {
        padding: '10px',
        borderRadius: '6px',
        border: '1px solid #ccc',
        fontSize: '16px',
        resize: 'vertical',
        minHeight: '80px',
    },
    button: {
        padding: '10px',
        backgroundColor: '#007BFF',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '16px',
    },
    button2: {
        width: '200px',
        padding: '10px',
        backgroundColor: '#e9e9e9',
        color: '#FF0000',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '16px',
    },
    clear: {
        display: 'flex',
        justifyContent: 'flex-end',
    },
    messageList: {
        listStyle: 'none',
        padding: 0,
    },
    messageItem: {
        padding: '10px',
        borderBottom: '1px solid #eee',
    },
    messageContent: {
        paddingTop: '5px',
        whiteSpace: 'pre-wrap',
        lineHeight: '1.8',
    },
    timestamp: {
        fontSize: '0.8em',
        color: '#999',
        marginTop: '4px',
    },
};

export default App;