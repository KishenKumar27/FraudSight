import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import openai
from fraud_detection import generate_sql_query, adjust_parameters_based_on_false_positives
import mysql.connector
import json

# Initialize FastAPI app
app = FastAPI()

# Connect to OpenAI API (assuming API key is set in your environment)
openai.api_key = "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"

# Database connection setup
connection = mysql.connector.connect(
    host="localhost",
    user="app_user",
    password="app_password",
    database="fraud_detection_db",
    port=3307
)

class UserQuery(BaseModel):
    user_intent: str

@app.on_event("startup")
async def startup_event():
    # Test the database connection at startup
    if not connection.is_connected():
        raise ConnectionError("Could not connect to the database.")

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection on shutdown
    if connection.is_connected():
        connection.close()

@app.post("/chat")
async def chat(user_query: UserQuery):
    user_intent = user_query.user_intent

    # Step 1: Get response from OpenAI for natural language interpretation
    try:
        openai_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_intent}],
            max_tokens=50
        )
        assistant_message = openai_response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    # Step 2: Check if intent involves fraud detection or table data generation
    if "table" in assistant_message.lower():
        # Adjust parameters based on historical false positives
        parameters = adjust_parameters_based_on_false_positives()
        
        # Generate SQL query based on the user intent and adjusted parameters
        query = generate_sql_query(user_intent, parameters)
        
        # Step 3: Execute the query and fetch data from MySQL
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result_data = cursor.fetchall()
        except mysql.connector.Error as db_error:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(db_error)}")
        
        # Step 4: Return table data as JSON response
        return {
            "message": "Here is the data related to your query.",
            "data": result_data,
            "is_fraud": any(detect_fraud(record) for record in result_data)  # Basic fraud indicator
        }

    # If no table data is required, respond with the assistant's message
    return {"message": assistant_message}


def detect_fraud(record: Dict[str, Optional[str]]) -> bool:
    """
    A basic function to flag potential fraud based on a few sample criteria.
    In production, this would be more complex.
    """
    # Example rule-based check (expand as needed):
    if record.get("amount") and float(record["amount"]) > 10000:  # Flag large amounts
        return True
    if record.get("location") and record["location"] not in ["User's usual locations"]:  # Flag unusual locations
        return True
    return False

# Add Uvicorn server start
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)