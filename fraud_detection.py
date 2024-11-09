import datetime
import json
import uvicorn
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List

# Define fraud parameters (mimicking the `fraud_parameters.json`)
# Load fraud parameters from the JSON file
def load_fraud_parameters():
    with open('fraud_parameters.json', 'r') as file:
        return json.load(file)

fraud_parameters = load_fraud_parameters()

# Database configuration
DATABASE_URL = "mysql+pymysql://app_user:app_password@localhost:3307/fraud_detection_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Pydantic models to receive user intent and send response
class UserIntent(BaseModel):
    user_intent: str

# Define database tables
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)
    gender = Column(String(10))
    country_of_residence = Column(String)
    occupation = Column(String)
    status = Column(String)
    income = Column(Float)
    phone_number = Column(String)
    account_creation_date = Column(DateTime)

class TradingTransaction(Base):
    __tablename__ = "trading_transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    transaction_type = Column(String)
    amount = Column(Float)
    currency = Column(String)
    transaction_time = Column(DateTime)
    location = Column(String)
    device_id = Column(String)
    ip_address = Column(String)
    user = relationship("User", back_populates="transactions")

User.transactions = relationship("TradingTransaction", back_populates="user")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3000",  # Frontend running locally (React default)
    "http://127.0.0.1:3000",  # Alternative for local development
    # Add more origins as needed for production or staging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend to make requests to the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request and response
class UserIntentRequest(BaseModel):
    user_intent: str

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: int
    amount: float
    transaction_type: str
    currency: str
    transaction_time: datetime.datetime
    location: str
    device_id: str
    ip_address: str
    flagged_parameters: List[str]
    flag_reason: str

# Process user_intent and query fraud data
@app.post("/process_intent", response_model=List[TransactionResponse])
async def process_intent(intent_request: UserIntentRequest):
    user_intent = intent_request.user_intent.lower()
    session = SessionLocal()

    try:
        # Determine query based on intent
        if "high risk" in user_intent:
            query = session.query(TradingTransaction).filter(TradingTransaction.amount > 10000)
        elif "unusual location" in user_intent:
            query = session.query(TradingTransaction).filter(TradingTransaction.location != "User's Usual Location")
        elif "suspicious frequency" in user_intent:
            query = session.query(TradingTransaction).filter(TradingTransaction.transaction_time > datetime.datetime.now() - datetime.timedelta(minutes=1))
        else:
            query = session.query(TradingTransaction)  # default query for general intent

        transactions = query.all()

        # Format results with flagged parameters
        results = []
        for txn in transactions:
            flagged_params = []
            flag_reason = ""

            # Add flagging logic based on fraud parameters
            if txn.amount > 10000:
                flagged_params.append(fraud_parameters[0]['parameter'])
                flag_reason += "Amount exceeds threshold. "
            if txn.location != "User's Usual Location":
                flagged_params.append(fraud_parameters[2]['parameter'])
                flag_reason += "Unusual location. "
            if txn.transaction_time.hour < 6 or txn.transaction_time.hour > 20:
                flagged_params.append(fraud_parameters[5]['parameter'])
                flag_reason += "Transaction during unusual hours. "

            results.append({
                "transaction_id": txn.transaction_id,
                "user_id": txn.user_id,
                "amount": txn.amount,
                "transaction_type": txn.transaction_type,
                "currency": txn.currency,
                "transaction_time": txn.transaction_time,
                "location": txn.location,
                "device_id": txn.device_id,
                "ip_address": txn.ip_address,
                "flagged_parameters": flagged_params,
                "flag_reason": flag_reason.strip()
            })
        
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Function to simulate fraud detection (you can replace this with more sophisticated logic)
def detect_fraud(transaction: dict) -> bool:
    # Simple rule: Randomly flag a transaction as fraud for this example
    return random.choice([True, False])

# Route to get fraud data based on user intent
@app.post("/get_fraud_data")
async def get_fraud_data(intent: UserIntent):
    user_intent = intent.user_intent.lower()
    
    # If the intent contains specific fraud-related keywords, return the fraud parameters table
    if "fraud parameters" in user_intent:
        return {"table": fraud_parameters}
    
    # If the intent is more specific or requires an analysis, return a basic analysis (for now)
    if "analyze" in user_intent or "check" in user_intent:
        # For simplicity, simulate a sample transaction for analysis
        sample_transaction = {
            "transaction_id": "T12345",
            "amount": 15000,
            "currency": "USD",
            "location": "US",
            "device_id": "device_5678",
            "ip_address": "192.168.1.1"
        }
        
        # Perform fraud detection analysis
        is_fraud = detect_fraud(sample_transaction)
        
        # Return a basic fraud analysis with 'is_fraud' field
        return {
            "answer": f"Analyzing the transaction with ID {sample_transaction['transaction_id']}...",
            "is_fraud": is_fraud,
            "transaction_details": sample_transaction
        }
    
    # Default response if no specific action is found
    return {"answer": "Sorry, I couldn't understand your request. Please try again with something related to fraud detection."}

# Add Uvicorn server start at the end
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)