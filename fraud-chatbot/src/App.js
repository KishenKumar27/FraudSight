import React, { useState } from 'react';
import Chatbot from './Chatbot';
import FraudParameterMenu from './FraudParameterMenu';

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen); // Toggle between showing and hiding the menu
  };

  return (
    <div style={styles.appContainer}>
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>Fraud Detection Chatbot</h1>
        <p style={styles.headerSubtitle}>Ask questions about fraud detection and get insights instantly!</p>
      </div>
      
      {/* Show the Chatbot only if the menu is not open */}
      {!isMenuOpen && <Chatbot />}
      
      {/* Show the Fraud Parameter Menu */}
      {isMenuOpen && <FraudParameterMenu />}
      
      <button onClick={toggleMenu} style={styles.toggleButton}>
        {isMenuOpen ? 'Back to Chatbot' : 'Open Fraud Parameter Menu'}
      </button>
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
    backgroundColor: '#e8f5e9',
    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
    padding: '20px',
    backgroundColor: '#00796b',
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
    color: '#d1f8e4',
    marginTop: '10px',
  },
  toggleButton: {
    backgroundColor: '#00796b',
    color: '#fff',
    padding: '10px 20px',
    cursor: 'pointer',
    borderRadius: '4px',
    border: 'none',
    marginTop: '20px',
  },
};

export default App;