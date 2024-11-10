import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import prompts
from intent_classifier import intent_classifier
from query_classifier import query_classifier

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your frontend to make requests to the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

def intent_generator(user_input):
    intent_clarifier = prompts.intent_gen
    
    intent_clarifier.append({"role": "user", "content": user_input})
    
    intent = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=prompts.intent_gen,
            max_tokens=500
    ).choices[0].message.content
    
    return intent
    

# Define request model
class ChatRequest(BaseModel):
    message: str

# Define the endpoint for handling chat requests
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        intent = intent_generator(request.message)
        
        isChartGenerated = intent_classifier(request.message)
        print(isChartGenerated)
        
        isQueryText = query_classifier(request.message)
        print(isQueryText)
        
        if isQueryText == "yes":
            isChartGenerated = "no"

                    
        if isChartGenerated == "no":
            # Create the chat conversation
            general_inquiry = prompts.general_inquiry

            # Add the user message to the conversation
            general_inquiry.append({"role": "user", "content": request.message})


            # Make the request to OpenAI's chat API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
                messages=general_inquiry,
            )
                    
            # Extract and return the assistant's reply
            assistant_message = response.choices[0].message.content
            
        else:
            table_inquiry = prompts.table_inquiry
            
            table_inquiry.append({"role": "user", "content": request.message})
            
            # Make the request to OpenAI's chat API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
                messages=table_inquiry,
            )
                    
            # Extract and return the assistant's reply
            assistant_message = response.choices[0].message.content
                           
        
        return {"response": assistant_message, "intent": intent, "isChartGenerated": isChartGenerated, "isQueryText": isQueryText}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add Uvicorn server start
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)