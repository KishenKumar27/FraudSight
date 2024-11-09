import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FraudParameterMenu = () => {
  const [parameters, setParameters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newParameter, setNewParameter] = useState({ parameter: '', description: '', example: '' });
  const [editParameterId, setEditParameterId] = useState(null);
  const [editParameterData, setEditParameterData] = useState({ parameter: '', description: '', example: '' });

  // Fetch fraud parameters
  const fetchFraudParameters = async () => {
    try {
      setLoading(true);
      const result = await axios.get('http://localhost:8002/fraud_parameters');
      console.log(result.data);
      setParameters(result.data);
      console.log(parameters);
      setError(null);
    } catch (error) {
      console.error("Error fetching fraud parameters:", error);
      setError("Failed to load fraud parameters. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFraudParameters();
  }, []);

  // Add a new fraud parameter
  const addFraudParameter = async (e) => {
    e.preventDefault();
    if (!newParameter.parameter || !newParameter.description || !newParameter.example) {
      setError("Parameter, description, and example are required.");
      return;
    }
  
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8002/fraud_parameters', {
        parameter: newParameter.parameter,
        description: newParameter.description,
        example: newParameter.example
      });
      setParameters((prev) => [...prev, response.data]); // Adds the new data to parameters
      setNewParameter({ parameter: '', description: '', example: '' }); // Reset form
      setError(null);
    } catch (error) {
      console.error("Error adding fraud parameter:", error);
      setError("Failed to add parameter. Please try again.");
    } finally {
      await fetchFraudParameters();
      setLoading(false);
    }
  };

  // Edit an existing fraud parameter
  const editFraudParameter = async (e) => {
    e.preventDefault();
    if (!editParameterData.parameter || !editParameterData.description) {
      setError("Parameter and description are required.");
      return;
    }

    try {
      setLoading(true); 
      const response = await axios.put(
        `http://localhost:8002/fraud_parameters/${editParameterId}`,
        {
          parameter: editParameterData.parameter,
          description: editParameterData.description,
          example: editParameterData.example
        }
      );
      const updatedParameters = parameters.map(param => 
        param.id === editParameterId ? response.data : param
      );
      setParameters(updatedParameters); // Set updated parameters
      setEditParameterId(null); // Clear edit mode
      setEditParameterData({ parameter: '', description: '', example: '' });
      setError(null);
    } catch (error) {
      console.error("Error editing fraud parameter:", error);
      setError("Failed to edit parameter. Please try again.");
    } finally {
      await fetchFraudParameters();
      setLoading(false);
    }
  };


    // Delete a fraud parameter
    const deleteFraudParameter = async (id) => {
        if (!window.confirm('Are you sure you want to delete this parameter?')) {
        return;
        }

        try {
        setLoading(true);
        await axios.delete(`http://localhost:8002/fraud_parameters/${id}`);
        setParameters((prev) => prev.filter((param) => param.id !== id));
        setEditParameterId(null);
        setError(null);
        } catch (error) {
        console.error("Error deleting fraud parameter:", error);
        setError("Failed to delete parameter. Please try again.");
        } finally {
        await fetchFraudParameters();
        setLoading(false);
        }
    };

    // Start editing a parameter
    const startEditing = (param) => {
        setEditParameterId(param.id);
        setEditParameterData({
            parameter: param.parameter,
            description: param.description,
            example: param.example || ''
        });
        setError(null);
    };

  // Cancel editing
  const cancelEditing = () => {
    setEditParameterId(null);
    setEditParameterData({ parameter: '', description: '', example: '' });
    setError(null);
  };

  // Rest of the component remains the same...
  return (
    <div style={styles.menuContainer}>
      <h2 style={styles.menuTitle}>Fraud Detection Parameters</h2>

      {error && <div style={styles.errorMessage}>{error}</div>}

      {/* Add Parameter Form */}
      <form onSubmit={addFraudParameter} style={styles.formContainer}>
        <h3 style={styles.formTitle}>Add New Parameter</h3>
        <input
          type="text"
          value={newParameter.parameter}
          onChange={(e) => setNewParameter({ ...newParameter, parameter: e.target.value })}
          placeholder="Parameter Name *"
          style={styles.input}
          required
        />
        <input
          type="text"
          value={newParameter.description}
          onChange={(e) => setNewParameter({ ...newParameter, description: e.target.value })}
          placeholder="Description *"
          style={styles.input}
          required
        />
        <input
          type="text"
          value={newParameter.example}
          onChange={(e) => setNewParameter({ ...newParameter, example: e.target.value })}
          placeholder="Example *"
          style={styles.input}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? 'Adding...' : 'Add Parameter'}
        </button>
      </form>

      {/* Parameters List */}
      <div style={styles.parametersWrapper}>
        {loading && !editParameterId && <div style={styles.loadingMessage}>Loading...</div>}

        <ul style={styles.parametersList}>
          {parameters.map((param) => (
            <li key={param.id} style={styles.parameterItem}>
              {editParameterId === param.id ? (
                <form onSubmit={editFraudParameter} style={styles.editForm}>
                  <input
                    type="text"
                    value={editParameterData.parameter}
                    onChange={(e) => setEditParameterData({ 
                      ...editParameterData, 
                      parameter: e.target.value 
                    })}
                    placeholder="Parameter Name *"
                    style={styles.editInput}
                    required
                  />
                  <input
                    type="text"
                    value={editParameterData.description}
                    onChange={(e) => setEditParameterData({ 
                      ...editParameterData, 
                      description: e.target.value 
                    })}
                    placeholder="Description *"
                    style={styles.editInput}
                    required
                  />
                  <input
                    type="text"
                    value={editParameterData.example}
                    onChange={(e) => setEditParameterData({ 
                      ...editParameterData, 
                      example: e.target.value 
                    })}
                    placeholder="Example"
                    style={styles.editInput}
                  />
                  <div style={styles.editActions}>
                    <button type="submit" style={styles.saveButton} disabled={loading}>
                      {loading ? 'Saving...' : 'Save'}
                    </button>
                    <button 
                      type="button" 
                      onClick={cancelEditing}
                      style={styles.cancelButton}
                      disabled={loading}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div style={styles.parameterContent}>
                    <strong style={styles.parameterName}>{param.parameter}</strong>
                    <p style={styles.parameterDescription}>{param.description}</p>
                    {param.example && (
                      <small style={styles.parameterExample}>Example: {param.example}</small>
                    )}
                  </div>
                  <div style={styles.actions}>
                    <button
                      onClick={() => startEditing(param)}
                      style={styles.editButton}
                      disabled={loading}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteFraudParameter(param.id)}
                      style={styles.deleteButton}
                      disabled={loading}
                    >
                      Delete
                    </button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const styles = {
    menuContainer: {
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px',
      boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      maxWidth: '800px',
      margin: '20px auto',
    },
    menuTitle: {
      fontSize: '1.8rem',
      marginBottom: '20px',
      color: '#00796b',
      textAlign: 'center',
    },
    formTitle: {
      fontSize: '1.2rem',
      marginBottom: '15px',
      color: '#00796b',
    },
    errorMessage: {
      backgroundColor: '#ffebee',
      color: '#c62828',
      padding: '10px',
      borderRadius: '4px',
      marginBottom: '20px',
    },
    loadingMessage: {
      textAlign: 'center',
      padding: '20px',
      color: '#666',
    },
    parametersWrapper: {
      maxHeight: '500px',
      overflowY: 'auto',
      marginTop: '20px',
      padding: '10px',
      backgroundColor: '#fff',
      borderRadius: '4px',
    },
    parametersList: {
      listStyleType: 'none',
      padding: 0,
      margin: 0,
    },
    parameterItem: {
      marginBottom: '15px',
      padding: '15px',
      backgroundColor: '#fff',
      borderRadius: '5px',
      boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e0e0e0',
    },
    parameterContent: {
      marginBottom: '10px',
    },
    parameterName: {
      display: 'block',
      fontSize: '1.1rem',
      marginBottom: '5px',
      color: '#00796b',
    },
    parameterDescription: {
      margin: '5px 0',
      color: '#333',
    },
    parameterExample: {
      display: 'block',
      color: '#666',
      marginTop: '5px',
    },
    formContainer: {
      backgroundColor: '#fff',
      padding: '20px',
      borderRadius: '4px',
      marginBottom: '20px',
      boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
    },
    editForm: {
      marginTop: '10px',
    },
    input: {
      width: '100%',
      padding: '10px',
      marginBottom: '10px',
      borderRadius: '4px',
      border: '1px solid #ccc',
      fontSize: '1rem',
    },
    editInput: {
      width: '100%',
      padding: '8px',
      marginBottom: '8px',
      borderRadius: '4px',
      border: '1px solid #ccc',
      fontSize: '0.9rem',
    },
    actions: {
      display: 'flex',
      gap: '10px',
      marginTop: '10px',
    },
    editActions: {
      display: 'flex',
      gap: '10px',
      marginTop: '10px',
    },
    button: {
      backgroundColor: '#00796b',
      color: '#fff',
      padding: '10px 20px',
      cursor: 'pointer',
      borderRadius: '4px',
      border: 'none',
      fontSize: '1rem',
      width: '100%',
    },
    editButton: {
      backgroundColor: '#ff9800',
      color: '#fff',
      padding: '8px 16px',
      cursor: 'pointer',
      borderRadius: '4px',
      border: 'none',
      flex: '1',
    },
    deleteButton: {
      backgroundColor: '#f44336',
      color: '#fff',
      padding: '8px 16px',
      cursor: 'pointer',
      borderRadius: '4px',
      border: 'none',
      flex: '1',
    },
    saveButton: {
      backgroundColor: '#4caf50',
      color: '#fff',
      padding: '8px 16px',
      cursor: 'pointer',
      borderRadius: '4px',
      border: 'none',
      flex: '1',
    },
    cancelButton: {
      backgroundColor: '#9e9e9e',
      color: '#fff',
      padding: '8px 16px',
      cursor: 'pointer',
      borderRadius: '4px',
      border: 'none',
      flex: '1',
    },
  };

export default FraudParameterMenu;
