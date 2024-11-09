// src/FraudTable.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FraudTable() {
  const [fraudData, setFraudData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch fraud data from the FastAPI backend
  useEffect(() => {
    axios.post('http://localhost:8000/process_intent', {
      user_intent: "Show me transactions with high amounts that may indicate fraud."
    })
    .then(response => {
      setFraudData(response.data);
      setLoading(false);
    })
    .catch(error => {
      console.error("There was an error fetching the data!", error);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Fraud Detection Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>User ID</th>
            <th>Amount</th>
            <th>Transaction Type</th>
            <th>Currency</th>
            <th>Transaction Time</th>
            <th>Location</th>
            <th>Device ID</th>
            <th>IP Address</th>
            <th>Flagged Parameters</th>
            <th>Flag Reason</th>
          </tr>
        </thead>
        <tbody>
          {fraudData.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.transaction_id}</td>
              <td>{transaction.user_id}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.transaction_type}</td>
              <td>{transaction.currency}</td>
              <td>{transaction.transaction_time}</td>
              <td>{transaction.location}</td>
              <td>{transaction.device_id}</td>
              <td>{transaction.ip_address}</td>
              <td>{transaction.flagged_parameters.join(", ")}</td>
              <td>{transaction.flag_reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FraudTable;