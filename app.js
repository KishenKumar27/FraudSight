import React, { useState } from 'react';
import Chatbot from 'react-chatbot-kit';
import axios from 'axios';
import 'react-chatbot-kit/build/main.css';

// Chatbot configuration
const config = {
  initialMessages: [
    {
      text: "Hello! I'm here to assist you with fraud detection analysis. What would you like to know?",
    },
  ],
  customStyles: {
    botMessageBox: {
      backgroundColor: '#3783A6',
    },
    chatButton: {
      backgroundColor: '#3783A6',
    },
  },
};

// Action to send user intent to FastAPI backend
const handleUserMessage = async (userMessage) => {
  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),  // Send message as JSON
    });

    const data = await response.json();

    if (data.response) {
      // Handle the assistant's response (update chat UI, etc.)
      console.log(data.response);
    } else if (data.error) {
      console.error(data.error);
    }
  } catch (error) {
    console.error("Error sending message:", error);
  }
};

// Render the chatbot
function App() {
  return (
    <div className="App">
      <h1>Fraud Detection Chatbot</h1>
      <Chatbot config={config} actionProvider={actionProvider} />
    </div>
  );
}

export default App;