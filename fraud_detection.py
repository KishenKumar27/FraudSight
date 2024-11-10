from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import Optional, Dict
import json
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
import google.generativeai as genai
from mysql_native_func import NATIVE_FUNC_MYSQL

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your frontend to make requests to the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "app_user",
    "password": "app_password",
    "database": "fraud_detection_db",
    "port": 3307
}

# Load fraud parameters from fraud_parameters.json
with open('fraud_parameters.json', 'r') as f:
    fraud_parameters = json.load(f)

# Convert fraud parameters into a prompt-friendly format
fraud_conditions_text = "\n".join([
    f"Parameter: {param['parameter']}\nDescription: {param['description']}\nExample: {param['example']}\n"
    for param in fraud_parameters
])

# Google Gemini API Configuration
genai.configure(api_key="AIzaSyC9oIGpFTbnySV3I3Qo_WF_90IjHZDibgI")

# Initialize database engine
def create_db_engine():
    """Create and return SQLAlchemy engine"""
    try:
        connection_url = f"mysql+pymysql://{DB_CONFIG['user']}:{quote_plus(DB_CONFIG['password'])}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

db_engine = create_db_engine()

# User intent model
class UserIntent(BaseModel):
    query: str

def execute_sql_query_with_retry(query: str, max_retries: int = 3) -> pd.DataFrame:
    """Attempt to execute SQL query with retries and return the result as a DataFrame."""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Establish a connection to the database engine
            with db_engine.connect() as connection:
                result = connection.execute(text(query))  # Execute the query
                # Fetch all rows and columns from the result
                rows = result.fetchall()
                columns = result.keys()  # Get column names
                # Convert the result into a DataFrame
                df = pd.DataFrame(rows, columns=columns)
                return df  # Return the DataFrame
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                # If all retries fail, raise an exception
                raise HTTPException(status_code=500, detail=f"Error executing SQL query after {max_retries} attempts: {str(e)}")
            print(f"Retrying query execution (attempt {retry_count}): {str(e)}")

def validate_sql_query(query: str) -> bool:
    """Validate SQL query for security and correctness"""
    dangerous_keywords = ['drop', 'truncate', 'delete', 'update', 'insert', 'alter', 'create']
    query_lower = query.lower()
    for keyword in dangerous_keywords:
        if keyword in query_lower:
            return False
    allowed_tables = ['users', 'trading_transactions']
    tables_referenced = [word.lower() for word in query_lower.split() if word.lower() in allowed_tables]
    if not tables_referenced:
        return False
    return True

# Generate SQL query using Gemini model
def generate_sql_query(user_intent: str) -> str:
    """Generate SQL query based on user intent using fraud parameters"""

    # Define the prompt that includes the fraud parameters and user intent
    prompt = f"""
You are a SQL expert. Based on the following fraud parameters, generate a SQL query that detects fraud based on user intent:

Given these database tables and their schemas:
    
1. `users` Table:
    - user_id (Primary Key)
    - name
    - email
    - Age
    - Gender
    - Country_of_residence
    - Occupation
    - Status
    - Income
    - Phone_Number
    - Account_Creation_Date

2. `trading_transactions` Table:
    - id (Primary Key)
    - transaction_id (Unique)
    - user_id (Foreign Key referencing User.user_id)
    - transaction_type
    - amount
    - currency
    - transaction_time
    - location
    - device_id
    - ip_address

Fraud Parameters:
{fraud_conditions_text}

The user intent is: "{user_intent}"

Requirements:
- Use only SELECT statements (no INSERT, UPDATE, DELETE, etc.).
- Include proper JOIN conditions when combining tables (e.g., JOIN users and trading_transactions).
- Use appropriate WHERE clauses for filtering, including fraud detection based on the parameters provided.
- Ensure correct date manipulation using NOW() or DATE_SUB() (e.g., t.transaction_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR)).
- Use standard SQL functions for date formatting (e.g., DATE_FORMAT for date-time fields).
- Include clear column aliases for readability.
- Optimize for performance with appropriate indexing columns.
- Handle NULL values appropriately.
- Include two new computed columns in the generated SQL query:
    1. `flag_reason`: A string column explaining why the transaction is flagged (based on the fraud parameters).
    2. `is_fraud`: A mandatory boolean column indicating whether the transaction is flagged as fraudulent (1 for fraud, 0 for no fraud).
- Add the `flag_reason` and `is_fraud` columns, which are not present in any table, and compute their values based on the data.
- Return only the SQL query without any explanations. Generate a complete SQL query, including the necessary logic for fraud detection based on the parameters listed above. Ensure that the `is_fraud` column is explicitly included as a mandatory part of the query.
- Only include the columns specified in the given database tables and their schemas.
- Ensure the `flag_reason` and `is_fraud` are not causing error `Unknown column 'flag_reason' in 'IN/ALL/ANY subquery'` in the SQL query.

SQL native Function

{NATIVE_FUNC_MYSQL}

"""

    try:
        # Call the Gemini API to generate the query
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(temperature=0.0))
        
        # Extract and return the generated SQL query from Gemini
        generated_query = response.text.strip()
        generated_query = generated_query.replace("```sql", "").replace("```", "")

        # Optionally, you could validate the generated query before returning
        if not validate_sql_query(generated_query):
            raise ValueError("Generated query failed validation")
        
        return generated_query
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SQL query with Gemini: {str(e)}")

def fix_sql_query_with_gemini(query: str) -> str:
    """Fix or optimize the MySQL SQL query using Gemini"""
    prompt = f"""
The following is an SQL query that needs to be fixed or optimized:

{query}

Please:
- Fix any syntax errors.
- Optimize the query for performance if possible.
- Ensure the query is safe and does not contain any dangerous operations (e.g., DROP, DELETE).
- Return the corrected and optimized SQL query.

Provide only the fixed query, without explanations.
"""

    try:
        # Send query to Gemini for fixing
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(temperature=0.0))
        fixed_query = response.text.strip()

        return fixed_query
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fixing SQL query with Gemini: {str(e)}")

def format_dataframe_response(df: pd.DataFrame) -> Dict:
    """Format DataFrame response with additional metadata"""
    return {
        "row_count": len(df),
        "columns": list(df.columns),
        "data": json.loads(df.to_json(orient="records", date_format="iso"))
    }

@app.post("/query/dataframe")
async def get_dataframe_response(user_intent: UserIntent):
    """Endpoint to return query results as a structured DataFrame"""
    try:
        sql_query = generate_sql_query(user_intent.query)
        
        # Try executing the query first
        try:
            df = execute_sql_query_with_retry(sql_query)
        except Exception:
            # If execution fails, attempt to fix the query
            fixed_sql_query = fix_sql_query_with_gemini(sql_query)
            df = execute_sql_query_with_retry(fixed_sql_query)
            sql_query = fixed_sql_query  # Update original query to the fixed one
        
        response = format_dataframe_response(df)
        
        return {
            "sql_query": sql_query,
            "results": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def convert_df_to_response_text_with_gemini(user_intent: str, df: pd.DataFrame) -> str:
    """
    Use Gemini to convert summarized DataFrame results into a paragraph that answers the user intent.
    
    Args:
        user_intent (str): The user's query or intent.
        df (pd.DataFrame): The DataFrame containing query results.

    Returns:
        str: A descriptive text paragraph that answers the user's intent based on the DataFrame data.
    """
    # Summarize the DataFrame to avoid passing too much data to Gemini
    summary = df.describe(include='all').to_json(orient="split", date_format="iso")

    # Prepare the prompt
    prompt = f"""
Given the following summarized data and a user intent, generate a paragraph response that answers the intent in a clear and descriptive manner. 

Summarized Data (in JSON format):
{summary}

User Intent:
"{user_intent}"

Requirements:
- Use the data to directly address the user's intent.
- Provide a coherent and concise summary in paragraph form.
- Avoid technical jargon unless necessary.
- If any data suggests fraud or unusual patterns, mention them in context.

Generate only the paragraph response text.
"""

    try:
        # Use Gemini to generate the response text
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(temperature=0.0))
        
        # Extract and return the response text from Gemini
        response_text = response.text.strip()
        return response_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response with Gemini: {str(e)}")

# Example endpoint using the Gemini-based conversion function
@app.post("/query/text")
async def get_text_response(user_intent: UserIntent):
    """Endpoint to return a Gemini-generated paragraph response to answer user intent"""
    try:
        sql_query = generate_sql_query(user_intent.query)
        
        # Execute the query with retry mechanism
        try:
            df = execute_sql_query_with_retry(sql_query)
        except HTTPException:
            # If execution fails after retries, attempt to fix the query
            fixed_sql_query = fix_sql_query_with_gemini(sql_query)
            df = execute_sql_query_with_retry(fixed_sql_query)
            sql_query = fixed_sql_query  # Update original query to the fixed one
        
        # Generate a Gemini-based paragraph response based on user intent and DataFrame content
        response_text = convert_df_to_response_text_with_gemini(user_intent.query, df)
        
        return {
            "sql_query": sql_query,
            "response": response_text,
            "record_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)