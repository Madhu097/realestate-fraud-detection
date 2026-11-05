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
from pathlib import Path
from typing import Tuple, List
import re

# Storage for text corpus
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CORPUS_FILE = DATA_DIR / "text_corpus.json"

# Similarity threshold
DUPLICATE_THRESHOLD = 0.88  # 88% similarity = likely stolen/copied text


def load_text_corpus() -> List[str]:
    """Load existing text descriptions from corpus"""
    if not CORPUS_FILE.exists():
        return []
    
    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [item.get('description', '') for item in data if item.get('description')]
    except Exception:
        return []


def save_to_corpus(description: str, metadata: dict = None):
    """Save description to corpus for future comparisons (avoiding exact duplicates)"""
    corpus = []
    
    if CORPUS_FILE.exists():
        try:
            with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
                corpus = json.load(f)
        except Exception:
            corpus = []
            
    # Check if exact text already exists
    clean_desc = description.strip()
    if clean_desc and not any(item.get('description', '').strip() == clean_desc for item in corpus):
        corpus.append({
            "description": clean_desc,
            "metadata": metadata or {}
        })
        try:
            with open(CORPUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(corpus[-50:], f, indent=2, ensure_ascii=False)
        except Exception:
            pass


def preprocess_text(text: str) -> str:
    """Preprocess text for comparison"""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()


def detect_duplicate_text(description: str, save_to_corpus_flag: bool = True) -> Tuple[float, int, List[str]]:
    """
    Detect if description is duplicate/similar to existing listings.
    """
    if not description or len(description.strip()) < 20:
        return 0.0, 0, []
        
    if not HAS_SKLEARN or not HAS_NUMPY:
        return 0.0, 0, []
    
    corpus = load_text_corpus()
    clean_desc = description.strip()
    
    if not corpus:
        if save_to_corpus_flag:
            save_to_corpus(clean_desc)
        return 0.0, 0, []
        
    new_text = preprocess_text(description)
    # Don't flag trivial short texts
    if len(new_text.split()) < 10:
        return 0.0, 0, []
        
    corpus_texts = [preprocess_text(text) for text in corpus if text.strip() != clean_desc]
    if not corpus_texts:
        if save_to_corpus_flag:
            save_to_corpus(clean_desc)
        return 0.0, 0, []
        
    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),
        max_features=1000,
        stop_words='english'
    )
    
    try:
        all_texts = corpus_texts + [new_text]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        new_vector = tfidf_matrix[-1]
        corpus_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(new_vector, corpus_vectors).flatten()
        max_sim = float(np.max(similarities)) if len(similarities) > 0 else 0.0
        
        # Save after checking to not self-match
        if save_to_corpus_flag:
            save_to_corpus(clean_desc)
            
        if max_sim >= DUPLICATE_THRESHOLD:
            similar_count = int(np.sum(similarities >= DUPLICATE_THRESHOLD))
            top_idx = int(np.argmax(similarities))
            similar_snippets = [corpus_texts[top_idx][:120]]
            # Duplicate score calibrated 0.6 - 0.95
            dup_score = 0.6 + (max_sim - DUPLICATE_THRESHOLD) / (1.0 - DUPLICATE_THRESHOLD) * 0.35
            return round(dup_score, 2), similar_count, similar_snippets
        else:
            return 0.0, 0, []
            
    except Exception as e:
        return 0.0, 0, []


def get_duplicate_explanation(
    duplicate_score: float,
    similar_count: int,
    similar_texts: List[str]
) -> str:
    """Generate human-readable explanation for duplicate detection"""
    if duplicate_score >= 0.8:
        return (
            f"⚠️ STOLEN / DUPLICATE DESCRIPTION: This description has {duplicate_score * 100:.0f}% "
            f"lexical similarity with an existing property listing in our registry. "
            f"Scammers frequently copy-paste descriptions from luxury listings."
        )
    elif duplicate_score > 0:
        return f"Partial description similarity detected ({duplicate_score * 100:.0f}%)."
    else:
        return "Description appears original. No unauthorized duplicate text detected."
