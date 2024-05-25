from sentence_transformers import SentenceTransformer
import pandas as pd
import os

# Ensure the file exists
file_path = 'emails.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist. Please check the file name and path.")

# Load your CSV file
df = pd.read_csv(file_path)

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert email contents to embeddings
embeddings = model.encode(df['Body'].astype(str).tolist())

# Add embeddings to the DataFrame
df['embeddings'] = embeddings.tolist()

# Save the updated DataFrame
df.to_csv("emails_with_embeddings.csv", index=False)
