from openai import OpenAI
import os
import prompts
from sklearn.metrics.pairwise import cosine_similarity

# Initialize OpenAI client
client = OpenAI(api_key="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")

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def query_classifier(user_input):
    query_classifier = prompts.query_class
    
    query_classifier.append({"role": "user", "content": user_input})
    
    query_class = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=prompts.query_class,
            max_tokens=500,
            temperature=0.0,
    ).choices[0].message.content
    
    print(query_class)
    
    query_class_vec = get_embedding(query_class)
    table_info_vec = get_embedding('reasoning about a particular data')
    req_general_inquiry = get_embedding('data-related inquiry or does not fit the criteria or general inquiry')
    
        
    # Compute cosine similarities
    similarity_query_info = cosine_similarity([query_class_vec], [table_info_vec])[0][0]
    similarity_general_inquiry = cosine_similarity([query_class_vec], [req_general_inquiry])[0][0]

    # Find the nearest vector
    if similarity_query_info > similarity_general_inquiry:
        nearest_vector = "reasoning about a particular data"
        highest_similarity = similarity_query_info
    else:
        nearest_vector = "data-related inquiry"
        highest_similarity = similarity_general_inquiry
                
    if nearest_vector == "reasoning about a particular data":
        isQueryGenerated = "yes"
    else:
        isQueryGenerated = "no"
        
    return isQueryGenerated
