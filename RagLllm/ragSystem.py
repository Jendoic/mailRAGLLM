from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index
index = faiss.read_index("email_index.faiss")

# Load the CSV file with emails and embeddings
df = pd.read_csv("emails_with_embeddings.csv")
df['embeddings'] = df['embeddings'].apply(eval)

def query_emails(query, top_k=5):
    # Convert the query to an embedding
    query_embedding = model.encode([query])

    # Search the FAISS index
    D, I = index.search(query_embedding, top_k)
    
    # Retrieve the relevant emails
    results = []
    for i in I[0]:
        if i != -1:  # Ensure it's a valid index
            email_data = df.iloc[i]
            results.append({
                'subject': email_data['Subject'],
                'from': email_data['From'],
                'date': email_data['Date'],
                'body': email_data['Body']
            })
    return results

# Example usage
# query = "what are the udemy Courses available?"
# results = query_emails(query)

# for result in results:
#     print("=" * 40)
#     print("Subject:", result['subject'])
#     print("From:", result['from'])
#     print("Date:", result['date'])
#     print("Body:", result['body'])
#     print("-" * 40)
