import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);  // Number of items per page
  const [totalPages, setTotalPages] = useState(1);  // Total number of pages

  const chatBoxRef = useRef(null);  // Create a reference for the chat box

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSendMessage = async () => {
    if (message.trim() === '') return;

    setChatHistory([...chatHistory, { user: message }]);
    setMessage('');
    setIsLoading(true);
    setCurrentPage(1);

    try {
      const response = await axios.post('http://localhost:8001/chat', { message });
      const { response: assistantResponse, intent, isChartGenerated, isQueryText } = response.data;

      if (isChartGenerated === 'yes') {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { assistant: assistantResponse },
        ]);

        const dataframeResponse = await axios.post('http://localhost:8000/query/dataframe', {
          query: intent,
        });

        if (dataframeResponse.data && Array.isArray(dataframeResponse.data.results.data) && dataframeResponse.data.results.data.length > 0) {
          const totalItems = dataframeResponse.data.results.data.length;
          setTotalPages(Math.ceil(totalItems / itemsPerPage));

          const startIndex = (currentPage - 1) * itemsPerPage;
          const currentPageData = dataframeResponse.data.results.data.slice(startIndex, startIndex + itemsPerPage);

          const dataframeTable = (
            <div>
              <table style={styles.table}>
                <thead>
                  <tr>
                    {Object.keys(currentPageData[0]).map((key) => (
                      <th key={key} style={styles.tableHeader}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {currentPageData.map((row, index) => (
                    <tr key={index}>
                      {Object.values(row).map((value, idx) => (
                        <td key={idx} style={styles.tableCell}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination Controls */}
              <div style={styles.pagination}>
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  style={styles.paginationButton}
                >
                  Previous
                </button>
                <span style={styles.pageNumber}>Page {currentPage} of {totalPages}</span>
                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  style={styles.paginationButton}
                >
                  Next
                </button>
              </div>
            </div>
          );

          setChatHistory((prevHistory) => [
            ...prevHistory,
            { dataframe: dataframeTable },
          ]);
        } else {
          setChatHistory((prevHistory) => [
            ...prevHistory,
            { error: 'No valid data returned from the dataframe query.' },
          ]);
        }
      } else if (isQueryText === 'yes') {
        const textResponse = await axios.post('http://localhost:8000/query/text', {
          query: intent,
        });
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { text: textResponse.data.response },
        ]);
      } else {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { text: assistantResponse },
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

  // Automatically add a 'hi' message on page load
  useEffect(() => {
    setChatHistory([
      { assistant: 'Hi! How can I assist you today with fraud detection?' },
      ...chatHistory,
    ]);
  }, []);

  // Scroll to bottom when chatHistory changes
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Handle Enter key press to send message
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent default behavior (new line)
      handleSendMessage();
    }
  };

  return (
    <div style={styles.chatContainer}>
      <div ref={chatBoxRef} style={styles.chatBox}>
        {chatHistory.map((entry, index) => (
          <div key={index} style={styles.messageContainer}>
            {entry.user && <div style={styles.userMessage}>{entry.user}</div>}
            {entry.assistant && <div style={styles.assistantMessage}>{entry.assistant}</div>}
            {entry.dataframe && <div style={styles.dataframeMessage}>{entry.dataframe}</div>}
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
          onKeyPress={handleKeyPress} // Handle Enter key press
        />
        <button onClick={handleSendMessage} disabled={isLoading} style={styles.sendButton}>
          <span style={styles.arrow}>&#8594;</span>  {/* Arrow symbol */}
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    width: '100%',
    maxWidth: '800px',  // Adjust max width for better responsiveness
    margin: '0 auto',
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 6px 15px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    height: '80vh',  // Set height for scrollable content
  },
  chatBox: {
    flexGrow: 1,
    maxHeight: '60vh',  // Limit chat history height
    overflowY: 'auto',
    marginBottom: '20px',
    paddingRight: '15px',
  },
  messageContainer: {
    marginBottom: '12px',
  },
  userMessage: {
    backgroundColor: '#e0f7fa',  // Light cyan for user messages
    padding: '12px',
    borderRadius: '10px',
    textAlign: 'left',
    wordBreak: 'break-word',
    fontSize: '1rem',
  },
  assistantMessage: {
    backgroundColor: '#c8e6c9',  // Soft green for assistant messages
    padding: '12px',
    borderRadius: '10px',
    textAlign: 'left',
    wordBreak: 'break-word',
    fontSize: '1rem',
  },
  dataframeMessage: {
    backgroundColor: '#f5f5f5',  // Light gray for data table
    padding: '12px',
    borderRadius: '10px',
    fontSize: '0.9rem',
    overflowX: 'auto',  // Allow horizontal scrolling for large tables
    maxHeight: '400px',
  },
  textMessage: {
    backgroundColor: '#ffecb3',  // Light yellow for additional information
    padding: '12px',
    borderRadius: '10px',
    fontSize: '0.9rem',
    wordBreak: 'break-word',
  },
  errorMessage: {
    backgroundColor: '#f8d7da',  // Red for errors
    padding: '12px',
    borderRadius: '10px',
    color: '#721c24',
    fontSize: '1rem',
    wordBreak: 'break-word',
  },
  inputContainer: {
    display: 'flex',
    alignItems: 'center',
    marginTop: '12px',
  },
  input: {
    width: '85%',
    padding: '12px',
    marginRight: '12px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    fontSize: '1rem',
    outline: 'none',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.05)',
  },
  sendButton: {
    padding: '12px 18px',
    backgroundColor: '#00796b',  // Green color for Send button
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1.5rem',
    transition: 'background-color 0.3s',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  arrow: {
    fontSize: '1.5rem',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    backgroundColor: '#00796b',
    padding: '10px',
    textAlign: 'left',
    fontWeight: 'bold',
    color: '#fff',
  },
  tableCell: {
    padding: '10px',
    textAlign: 'left',
    borderBottom: '1px solid #ddd',
    wordBreak: 'break-word',
  },
  pagination: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: '20px',
  },
  paginationButton: {
    padding: '10px 15px',
    backgroundColor: '#00796b',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
    transition: 'background-color 0.3s',
  },
  pageNumber: {
    alignSelf: 'center',
    fontSize: '1rem',
    margin: '0 15px',
  },
};

export default Chatbot;