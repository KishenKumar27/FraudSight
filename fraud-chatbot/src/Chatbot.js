import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);  // Number of items per page
  const [totalPages, setTotalPages] = useState(1);  // Total number of pages

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
      const { response: assistantResponse, intent, isChartGenerated } = response.data;

      // Display the assistant's reply
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { assistant: assistantResponse },
      ]);


      // Call the appropriate query endpoint based on isChartGenerated
      if (isChartGenerated === 'yes') {
        const dataframeResponse = await axios.post('http://localhost:8000/query/dataframe', {
          query: intent,
        });

        if (dataframeResponse.data && Array.isArray(dataframeResponse.data.results.data) && dataframeResponse.data.results.data.length > 0) {
          // Pagination logic
          const totalItems = dataframeResponse.data.results.data.length;
          setTotalPages(Math.ceil(totalItems / itemsPerPage));

          const startIndex = (currentPage - 1) * itemsPerPage;
          const currentPageData = dataframeResponse.data.results.data.slice(startIndex, startIndex + itemsPerPage);

          // Convert the dataframe response to table format
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
      } else {
        const textResponse = await axios.post('http://localhost:8000/query/text', {
          query: intent,
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
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '10px',
  },
  tableHeader: {
    backgroundColor: '#f2f2f2',
    padding: '8px',
    textAlign: 'left',
    fontWeight: 'bold',
  },
  tableCell: {
    padding: '8px',
    textAlign: 'left',
    borderBottom: '1px solid #ddd',
  },
  pagination: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: '10px',
  },
  paginationButton: {
    padding: '8px 12px',
    margin: '0 5px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  pageNumber: {
    alignSelf: 'center',
    margin: '0 10px',
  },
};

export default Chatbot;