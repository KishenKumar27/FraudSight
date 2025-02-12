from together import Together
from sentence_transformers import SentenceTransformer
import os
import prompts
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = Together(api_key=os.getenv('API_KEY'))
emb_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

def get_embedding(text, model=emb_model):
   text = text.replace("\n", " ")
   sentences = [f'search_query: {text}']
   embeddings = model.encode(sentences)
   return embeddings[0]

def intent_classifier(user_input):
    intent_classifier = prompts.intent_class
    
    intent_classifier.append({"role": "user", "content": user_input})
    
    intent_class = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",  # You can use gpt-4 if you have access
            messages=prompts.intent_class,
            max_tokens=500,
            temperature=0.0,
    ).choices[0].message.content
    
    print(intent_class)
    
    intent_class_vec = get_embedding(intent_class)
    table_info_vec = get_embedding('data-related inquiry')
    req_general_inquiry = get_embedding('requires general inquiry')
    
        
    # Compute cosine similarities
    similarity_table_info = cosine_similarity([intent_class_vec], [table_info_vec])[0][0]
    similarity_general_inquiry = cosine_similarity([intent_class_vec], [req_general_inquiry])[0][0]

    # Find the nearest vector
    if similarity_table_info > similarity_general_inquiry:
        nearest_vector = "data_info"
        highest_similarity = similarity_table_info
    else:
        nearest_vector = "req_general_inquiry"
        highest_similarity = similarity_general_inquiry
        
    isChartGenerated = ""
        
    if nearest_vector == "data_info":
        isChartGenerated = "yes"
    else:
        isChartGenerated = "no"
        
    return isChartGenerated
