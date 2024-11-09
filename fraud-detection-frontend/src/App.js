import React, { useState } from "react";
import { Chatbot } from "react-chatbot-kit";
import config from "./config";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import './App.css';  // Import the CSS file

const ChatBotApp = () => {
  const [messages, setMessages] = useState(config.initialMessages);

  return (
    <div className="chatbot-container">
      <div className="chat-messages">
        {/* Render the messages dynamically */}
        {messages.map((message, index) => (
          <div
            key={index}
            className={message.type === "user" ? "user-message" : "bot-message"}
          >
            {message.text}
          </div>
        ))}
      </div>

      <div className="input-container">
        <input
          type="text"
          id="user-input"
          placeholder="Type your message here..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              // Send user message to backend
              const userInput = e.target.value;
              setMessages([
                ...messages,
                { text: userInput, type: "user" },
              ]);

              // Send to backend and get response
              // Assuming we already have actionProvider to handle the interaction
              new ActionProvider(
                (message) => {
                  setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: message, type: "bot" },
                  ]);
                }
              ).handleUserMessage(userInput);

              e.target.value = "";  // Clear the input field
            }
          }}
        />
        <button
          onClick={() => {
            const userInput = document.getElementById("user-input").value;
            if (userInput) {
              setMessages([
                ...messages,
                { text: userInput, type: "user" },
              ]);
              new ActionProvider(
                (message) => {
                  setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: message, type: "bot" },
                  ]);
                }
              ).handleUserMessage(userInput);

              document.getElementById("user-input").value = ""; // Clear input
            }
          }}
        >
          &#10148;
        </button>
      </div>
    </div>
  );
};

export default ChatBotApp;