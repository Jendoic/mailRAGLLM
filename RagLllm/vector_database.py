import faiss
import numpy as np
import pandas as pd

# Load the DataFrame
df = pd.read_csv("emails_with_embeddings.csv")

# Check if the embeddings column exists and has the correct format
if 'embeddings' not in df.columns:
    raise ValueError("Embeddings column not found in the CSV file.")
if df['embeddings'].isnull().any():
    raise ValueError("There are null values in the embeddings column.")
if not isinstance(df['embeddings'].iloc[0], str):
    raise ValueError("Embeddings column does not contain string representations of lists.")

# Convert the string representations of lists back to actual lists
df['embeddings'] = df['embeddings'].apply(eval)

# Convert embeddings to a numpy array
embeddings = np.array(df['embeddings'].tolist())

# Check the shape of the embeddings array
if embeddings.ndim != 2:
    raise ValueError(f"Embeddings array has incorrect dimensions: {embeddings.shape}")

# Create a FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save the index to disk
faiss.write_index(index, "email_index.faiss")
