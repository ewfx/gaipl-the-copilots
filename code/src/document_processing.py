import os
import faiss
import numpy as np
from langchain.document_loaders import TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

# Set OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key_here"

# Load and process documents
def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith(".txt"):
            loader = TextLoader(file_path)
        elif filename.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            continue  # Skip unsupported files
        
        documents.extend(loader.load())  
    return documents

# Split long documents into smaller chunks
def split_documents(docs, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)

# Convert chunks to FAISS embeddings
def create_faiss_index(chunks):
    embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    text_list = [chunk.page_content for chunk in chunks]
    vectors = np.array([embeddings_model.embed_query(text) for text in text_list]).astype("float32")
    
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    
    faiss.write_index(index, "faiss_index/knowledge_index.faiss")
    with open("faiss_index/text_data.txt", "w") as f:
        f.write("\n".join(text_list))
    
    print("FAISS index updated successfully.")

# Run the nightly process
def update_documents():
    docs = load_documents("knowledge_base/")
    chunks = split_documents(docs)
    create_faiss_index(chunks)

if __name__ == "__main__":
    update_documents()
