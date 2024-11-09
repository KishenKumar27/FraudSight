from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can specify frontend domain here)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the structure for user input
class UserInput(BaseModel):
    question: str  # e.g., "Is this transaction fraudulent?"
    transaction_id: Optional[str] = None
    amount: Optional[float] = None

# Mock transaction data (in real application, replace with database connection)
transactions = pd.DataFrame({
    "user_id": ["001", "002", "003", "004", "005"],
    "amount": [500, 1200, 50, 300, 2000],  # Example amounts
    "fraud_flag": [0, 1, 0, 0, 1]  # 1 indicates flagged transactions
})

# Train a simple Isolation Forest model for fraud detection
model = IsolationForest(n_estimators=100, contamination=0.2, random_state=42)
model.fit(transactions[['amount']])  # Use amount as a feature for anomaly detection

@app.post("/analyze")
def analyze_input(data: UserInput):
    question = data.question.lower()
    
    if "fraud" in question:
        if data.amount:
            # Perform fraud risk analysis
            risk_score = model.decision_function([[data.amount]])[0]
            is_fraud = model.predict([[data.amount]])[0] == -1
            response = {
                "response_type": "text",
                "risk_score": risk_score,
                "is_fraud": is_fraud,
                "message": "High fraud risk!" if is_fraud else "Low fraud risk."
            }
        else:
            raise HTTPException(status_code=400, detail="Transaction amount is required for fraud check.")
        return response
    
    elif "trend" in question or "chart" in question:
        # Generate a simple chart to visualize fraud trends
        plt.bar(transactions['user_id'], transactions['amount'], color=['red' if f else 'blue' for f in transactions['fraud_flag']])
        plt.xlabel("User ID")
        plt.ylabel("Transaction Amount")
        plt.title("Transaction Amounts and Fraud Flags")

        # Save chart as an image and encode it
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        
        return {"response_type": "chart", "chart": img_str}

    else:
        return {"response_type": "text", "message": "Sorry, I couldn't understand the question. Try asking about fraud risk or trends."}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        h11_max_incomplete_event_size=5000000000,
        timeout_keep_alive=10,
    )