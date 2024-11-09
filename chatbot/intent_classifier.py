from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Add the user message to the conversation
conversation.append({"role": "user", "content": request.message})


# Make the request to OpenAI's chat API
response = client.chat.completions.create(
model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
messages=conversation
)
        