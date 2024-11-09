import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSendMessage = async () => {
    if (message.trim() === '') return;
    
    // Display the user's message in the chat history
    setChatHistory([...chatHistory, { user: message }]);
    setMessage('');
    setIsLoading(true);

    try {
      // Send the message to the FastAPI chatbot endpoint
      const response = await axios.post('http://localhost:8001/chat', { message });
      const { response: assistantResponse, userIntent, isChartGenerated } = response.data;

      // Display the assistant's reply
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { assistant: assistantResponse },
      ]);

      console.log(userIntent)

      // Call the appropriate query endpoint based on isChartGenerated
      if (isChartGenerated === 'yes') {
        const dataframeResponse = await axios.post('http://localhost:8000/query/dataframe', {
          query: assistantResponse,
        });
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { dataframe: dataframeResponse.data.results },
        ]);
      } else {
        const textResponse = await axios.post('http://localhost:8000/query/text', {
          query: assistantResponse,
        });
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { text: textResponse.data.response },
        ]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { error: 'Something went wrong. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.chatBox}>
        {chatHistory.map((entry, index) => (
          <div key={index} style={styles.messageContainer}>
            {entry.user && <div style={styles.userMessage}>{entry.user}</div>}
            {entry.assistant && <div style={styles.assistantMessage}>{entry.assistant}</div>}
            {entry.dataframe && <div style={styles.dataframeMessage}>Data: {JSON.stringify(entry.dataframe)}</div>}
            {entry.text && <div style={styles.textMessage}>{entry.text}</div>}
            {entry.error && <div style={styles.errorMessage}>{entry.error}</div>}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={message}
          onChange={handleMessageChange}
          placeholder="Ask about fraud detection..."
          style={styles.input}
        />
        <button onClick={handleSendMessage} disabled={isLoading} style={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    width: '400px',
    margin: '0 auto',
    padding: '20px',
    backgroundColor: '#f9f9f9',
    borderRadius: '10px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
  },
  chatBox: {
    maxHeight: '400px',
    overflowY: 'auto',
    marginBottom: '20px',
  },
  messageContainer: {
    marginBottom: '10px',
  },
  userMessage: {
    backgroundColor: '#d1e7fd',
    padding: '10px',
    borderRadius: '10px',
    textAlign: 'left',
  },
  assistantMessage: {
    backgroundColor: '#e8f4e8',
    padding: '10px',
    borderRadius: '10px',
    textAlign: 'left',
  },
  dataframeMessage: {
    backgroundColor: '#f1f1f1',
    padding: '10px',
    borderRadius: '10px',
    fontSize: '0.85rem',
  },
  textMessage: {
    backgroundColor: '#fff3cd',
    padding: '10px',
    borderRadius: '10px',
    fontSize: '0.85rem',
  },
  errorMessage: {
    backgroundColor: '#f8d7da',
    padding: '10px',
    borderRadius: '10px',
    color: '#721c24',
  },
  inputContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  input: {
    width: '80%',
    padding: '10px',
    marginRight: '10px',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  sendButton: {
    padding: '10px 15px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default Chatbot;