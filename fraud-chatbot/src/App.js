import React from 'react';
import Chatbot from './Chatbot';

function App() {
  return (
    <div style={styles.appContainer}>
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>Fraud Detection Chatbot</h1>
        <p style={styles.headerSubtitle}>Ask questions about fraud detection and get insights instantly!</p>
      </div>
      <Chatbot />
    </div>
  );
}

const styles = {
  appContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#e8f5e9',  // Light green background for a calm, professional feel
    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif', // Modern sans-serif font
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
    padding: '20px',
    backgroundColor: '#00796b', // Deep green for the header
    borderRadius: '10px',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '800px',
  },
  headerTitle: {
    fontSize: '2.5rem',
    color: '#fff',
    margin: '0',
    fontWeight: 'bold',
    letterSpacing: '1px',
  },
  headerSubtitle: {
    fontSize: '1.2rem',
    color: '#d1f8e4',  // Soft light green for the subtitle
    marginTop: '10px',
  },
};

export default App;