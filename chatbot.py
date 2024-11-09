import uvicorn
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Replace with your OpenAI API key
openai.api_key = "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"

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3001",  # Frontend running locally (React default)
    "http://127.0.0.1:3001",  # Alternative for local development
    # Add more origins as needed for production or staging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend to make requests to the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define request model
class ChatRequest(BaseModel):
    message: str

# Define the endpoint for handling chat requests
@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    
    # Create the chat conversation
    conversation = [
        {"role": "system", "content": "You are a helpful fraud detection assistant."},
        {"role": "user", "content": user_message}
    ]

    try:
        # Make the request to OpenAI's chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=conversation
        )
        
        # Extract and return the assistant's reply
        assistant_message = response['choices'][0]['message']['content']
        return {"response": assistant_message}

    except Exception as e:
        return {"error": str(e)}
    
# Add Uvicorn server start at the end
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)