"""
Vector database module for storing and retrieving website content.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional


class VectorDatabase:
    """Manages vector database operations using ChromaDB."""
    
    def __init__(self, collection_name: str = "website_research"):
        """
        Initialize the vector database.
        
        Args:
            collection_name: Name of the collection to use
        """
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        self.collection_name = collection_name
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the collection."""
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"Using existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Website research content storage"}
            )
            print(f"Created new collection: {self.collection_name}")
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to the vector database.
        
        Args:
            documents: List of dictionaries with 'url', 'title', and 'content'
        """
        if not documents:
            print("No documents to add")
            return
        
        ids = [doc['url'] for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [{'title': doc['title'], 'url': doc['url']} for doc in documents]
        
        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to the database")
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """
        Search for relevant documents in the database.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def get_all_documents(self) -> Dict:
        """
        Get all documents from the collection.
        
        Returns:
            Dictionary containing all documents
        """
        return self.collection.get()
    
    def reset_collection(self):
        """Reset the collection by deleting and recreating it."""
        self.client.delete_collection(name=self.collection_name)
        self._initialize_collection()
        print(f"Reset collection: {self.collection_name}")
