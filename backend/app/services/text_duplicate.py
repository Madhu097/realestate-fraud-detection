"""
Text Duplicate Detection Service
Detects duplicate or highly similar listing descriptions using TF-IDF and cosine similarity
"""
from app.utils.ml_imports import HAS_SKLEARN, HAS_NUMPY, np, get_unavailable_message

# Conditional imports
if HAS_SKLEARN:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

import json
import os
from typing import Tuple, List
import re

# Storage for text corpus
CORPUS_FILE = "app/data/text_corpus.json"

# Similarity threshold
DUPLICATE_THRESHOLD = 0.8  # 80% similarity = likely duplicate


def load_text_corpus() -> List[str]:
    """Load existing text descriptions from corpus"""
    if not os.path.exists(CORPUS_FILE):
        return []
    
    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [item['description'] for item in data]
    except:
        return []


def save_to_corpus(description: str, metadata: dict = None):
    """Save description to corpus for future comparisons"""
    corpus = []
    
    if os.path.exists(CORPUS_FILE):
        try:
            with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
                corpus = json.load(f)
        except:
            corpus = []
    
    # Add new description
    corpus.append({
        "description": description,
        "metadata": metadata or {}
    })
    
    # Save to file
    os.makedirs(os.path.dirname(CORPUS_FILE), exist_ok=True)
    with open(CORPUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)


def preprocess_text(text: str) -> str:
    """
    Preprocess text for better comparison
    
    Args:
        text: Raw text string
        
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    return text.strip()


def detect_duplicate_text(description: str, save_to_corpus_flag: bool = True) -> Tuple[float, int, List[str]]:
    """
    Detect if description is duplicate/similar to existing listings
    
    Uses TF-IDF vectorization and cosine similarity
    
    Args:
        description: Listing description to analyze
        save_to_corpus_flag: Whether to save this description to corpus
        
    Returns:
        tuple: (duplicate_score, similar_count, similar_texts)
            - duplicate_score (float): 0.0 to 1.0, highest similarity found
            - similar_count (int): Number of similar descriptions found
            - similar_texts (list): List of similar text snippets (first 100 chars)
    """
    # Check if ML libraries are available
    if not HAS_SKLEARN or not HAS_NUMPY:
        # Basic keyword-based duplicate detection as fallback
        if save_to_corpus_flag:
            save_to_corpus(description)
        return 0.2, 0, [get_unavailable_message()]
    
    # Load existing corpus
    corpus = load_text_corpus()
    
    if not corpus:
        # No existing data to compare against
        if save_to_corpus_flag:
            save_to_corpus(description)
        return 0.0, 0, []
    
    # Preprocess texts
    new_text = preprocess_text(description)
    corpus_texts = [preprocess_text(text) for text in corpus]
    
    # Create TF-IDF vectorizer
    # Use character n-grams for better similarity detection
    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),  # Unigrams and bigrams
        max_features=1000,
        stop_words='english'
    )
    
    try:
        # Fit vectorizer on corpus + new text
        all_texts = corpus_texts + [new_text]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Get vector for new text (last one)
        new_vector = tfidf_matrix[-1]
        
        # Get vectors for corpus (all except last)
        corpus_vectors = tfidf_matrix[:-1]
        
        # Calculate cosine similarity
        similarities = cosine_similarity(new_vector, corpus_vectors).flatten()
        
        # Find similar texts
        similar_indices = np.where(similarities >= DUPLICATE_THRESHOLD)[0]
        similar_count = len(similar_indices)
        
        # Get highest similarity score
        max_similarity = float(np.max(similarities)) if len(similarities) > 0 else 0.0
        
        # Get similar text snippets for explanation
        similar_texts = []
        for idx in similar_indices[:3]:  # Top 3 similar texts
            text_snippet = corpus[idx][:100] + "..." if len(corpus[idx]) > 100 else corpus[idx]
            similarity_percent = similarities[idx] * 100
            similar_texts.append(f"{similarity_percent:.1f}% similar: \"{text_snippet}\"")
        
        # Save to corpus if requested
        if save_to_corpus_flag:
            save_to_corpus(description)
        
        return max_similarity, similar_count, similar_texts
        
    except Exception as e:
        print(f"Error in duplicate detection: {e}")
        # On error, save to corpus and return safe values
        if save_to_corpus_flag:
            save_to_corpus(description)
        return 0.0, 0, []


def get_duplicate_explanation(duplicate_score: float, similar_count: int, similar_texts: List[str]) -> str:
    """
    Generate human-readable explanation for duplicate detection
    
    Args:
        duplicate_score: Similarity score (0-1)
        similar_count: Number of similar descriptions
        similar_texts: List of similar text snippets
        
    Returns:
        str: Clear explanation
    """
    if duplicate_score < 0.5:
        return "The description appears to be unique. No significant similarity to existing listings detected."
    
    elif duplicate_score < DUPLICATE_THRESHOLD:
        return (
            f"The description shows moderate similarity ({duplicate_score*100:.1f}%) to existing listings. "
            f"This may indicate common phrasing but is not flagged as a duplicate."
        )
    
    else:
        # High similarity - likely duplicate
        explanation = (
            f"The description is highly similar ({duplicate_score*100:.1f}%) to {similar_count} existing listing(s), "
            f"indicating a possible duplicate or copy-paste fraud. "
        )
        
        if similar_texts:
            explanation += "Similar descriptions found:\n" + "\n".join(similar_texts[:2])
        
        return explanation
