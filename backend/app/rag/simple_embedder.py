"""
Simple embedding system for products without external dependencies.
Uses TF-IDF-like approach for keyword matching.
"""
import json
import re
from typing import List, Dict, Any
from pathlib import Path
from collections import Counter
import math


class SimpleEmbedder:
    """
    Simple text embedder using TF-IDF approach.
    Good enough for demo purposes without requiring heavy ML libraries.
    """

    def __init__(self):
        self.idf_scores = {}
        self.documents = []
        self.vocab = set()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 2]  # Filter short words

    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """Compute term frequency."""
        counter = Counter(tokens)
        total = len(tokens)
        return {word: count / total for word, count in counter.items()}

    def fit(self, documents: List[str]):
        """Fit the embedder on a corpus of documents."""
        self.documents = documents
        
        # Tokenize all documents
        tokenized_docs = [self._tokenize(doc) for doc in documents]
        
        # Build vocabulary
        for tokens in tokenized_docs:
            self.vocab.update(tokens)
        
        # Compute IDF scores
        doc_count = len(documents)
        word_doc_count = Counter()
        
        for tokens in tokenized_docs:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                word_doc_count[token] += 1
        
        # IDF = log(total_documents / documents_containing_word)
        for word, count in word_doc_count.items():
            self.idf_scores[word] = math.log(doc_count / count)

    def embed(self, text: str) -> List[float]:
        """
        Create a simple TF-IDF vector for the text.
        Returns a fixed-size vector based on vocabulary.
        """
        tokens = self._tokenize(text)
        tf_scores = self._compute_tf(tokens)
        
        # Create vector: use sorted vocab for consistent ordering
        vocab_list = sorted(self.vocab)
        vector = []
        
        for word in vocab_list:
            tf = tf_scores.get(word, 0.0)
            idf = self.idf_scores.get(word, 0.0)
            tfidf = tf * idf
            vector.append(tfidf)
        
        # Normalize vector
        magnitude = math.sqrt(sum(v ** 2 for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        
        return vector

    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        return max(0.0, min(1.0, dot_product))  # Clamp to [0, 1]


class ProductVectorStore:
    """
    Vector store for product data using simple embeddings.
    """

    def __init__(self, products_file: str = None):
        self.embedder = SimpleEmbedder()
        self.products = []
        self.product_vectors = []
        
        if products_file:
            self.load_products(products_file)

    def load_products(self, products_file: str):
        """Load products from JSON file."""
        file_path = Path(products_file)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Products file not found: {products_file}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            self.products = json.load(f)
        
        # Create searchable text for each product
        product_texts = []
        for product in self.products:
            # Combine relevant fields into searchable text
            text_parts = [
                product.get('name', ''),
                product.get('description', ''),
                product.get('category', ''),
                product.get('subcategory', ''),
                product.get('material', ''),
                ' '.join(product.get('features', [])),
                ' '.join(product.get('colors', []))
            ]
            text = ' '.join(text_parts)
            product_texts.append(text)
        
        # Fit embedder and create vectors
        self.embedder.fit(product_texts)
        self.product_vectors = [self.embedder.embed(text) for text in product_texts]
        
        print(f"✅ Loaded {len(self.products)} products into vector store")

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for products matching the query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of products with similarity scores
        """
        if not self.products:
            return []
        
        # Create query vector
        query_vector = self.embedder.embed(query)
        
        # Compute similarities
        similarities = []
        for idx, product_vector in enumerate(self.product_vectors):
            similarity = self.embedder.similarity(query_vector, product_vector)
            similarities.append((idx, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top K results
        results = []
        for idx, score in similarities[:top_k]:
            product = self.products[idx].copy()
            product['similarity_score'] = round(score, 3)
            results.append(product)
        
        return results

    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products."""
        return self.products.copy()

    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Get a specific product by ID."""
        for product in self.products:
            if product.get('id') == product_id:
                return product.copy()
        return None


# Singleton instance
_vector_store = None


def get_vector_store() -> ProductVectorStore:
    """Get or create the singleton vector store instance."""
    global _vector_store
    if _vector_store is None:
        products_file = Path(__file__).parent.parent.parent.parent / "data" / "products_drinkware.json"
        _vector_store = ProductVectorStore(str(products_file))
    return _vector_store

