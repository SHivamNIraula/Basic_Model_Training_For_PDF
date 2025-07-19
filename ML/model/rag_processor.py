import os
import pickle
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class RAGProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.index = None
        self.documents = []
        self.embeddings = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
        return text
    
    def chunk_text(self, text: str) -> List[Document]:
        """Split text into chunks."""
        documents = self.text_splitter.split_text(text)
        return [Document(page_content=doc) for doc in documents]
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for text chunks."""
        embeddings = self.embedding_model.encode(texts)
        return np.array(embeddings)
    
    def create_faiss_index(self, embeddings: np.ndarray) -> faiss.IndexFlatL2:
        """Create FAISS index for similarity search."""
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        return index
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF and create RAG system."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {"error": "Failed to extract text from PDF"}
        
        # Chunk text
        documents = self.chunk_text(text)
        self.documents = documents
        
        # Generate embeddings
        texts = [doc.page_content for doc in documents]
        embeddings = self.generate_embeddings(texts)
        self.embeddings = embeddings
        
        # Create FAISS index
        self.index = self.create_faiss_index(embeddings)
        
        return {
            "status": "success",
            "num_chunks": len(documents),
            "embedding_dimension": embeddings.shape[1]
        }
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if self.index is None:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    "content": self.documents[idx].page_content,
                    "similarity_score": float(1 / (1 + distance)),  # Convert distance to similarity
                    "rank": i + 1
                })
        
        return results
    
    def save_index(self, filepath: str):
        """Save the FAISS index and documents to disk."""
        data = {
            'index': self.index,
            'documents': self.documents,
            'embeddings': self.embeddings
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load_index(self, filepath: str):
        """Load the FAISS index and documents from disk."""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            self.index = data['index']
            self.documents = data['documents']
            self.embeddings = data['embeddings']
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def get_answer_with_context(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Get relevant context for answering the query."""
        similar_docs = self.similarity_search(query, k)
        
        if not similar_docs:
            return {"error": "No relevant documents found"}
        
        context = "\n\n".join([doc["content"] for doc in similar_docs])
        
        return {
            "query": query,
            "context": context,
            "similar_documents": similar_docs,
            "context_length": len(context)
        }