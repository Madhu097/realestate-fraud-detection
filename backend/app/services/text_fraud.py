"""
Text Fraud Detection Service
Combines duplicate detection and manipulation detection for comprehensive text fraud analysis
"""
from typing import Tuple, List
from app.services.text_duplicate import (
    detect_duplicate_text,
    get_duplicate_explanation
)
from app.services.text_manipulation import (
    detect_promotional_language,
    get_manipulation_explanation,
    analyze_text_length
)


def detect_text_fraud(
    title: str,
    description: str,
    save_to_corpus: bool = True
) -> Tuple[float, List[str]]:
    """
    Comprehensive text fraud detection
    
    Combines:
    1. Duplicate detection (TF-IDF + cosine similarity)
    2. Promotional language detection (rule-based keywords)
    3. Text length analysis
    
    Args:
        title: Listing title
        description: Listing description
        save_to_corpus: Whether to save description to corpus
        
    Returns:
        tuple: (text_fraud_score, explanations)
            - text_fraud_score (float): 0.0 to 1.0, combined fraud score
            - explanations (list): List of human-readable explanations
    """
    explanations = []
    scores = []
    
    # Combine title and description for analysis
    full_text = f"{title}. {description}"
    
    # ============================================================
    # 1. DUPLICATE DETECTION (TF-IDF + Cosine Similarity)
    # ============================================================
    try:
        duplicate_score, similar_count, similar_texts = detect_duplicate_text(
            description=full_text,
            save_to_corpus_flag=save_to_corpus
        )
        
        duplicate_explanation = get_duplicate_explanation(
            duplicate_score=duplicate_score,
            similar_count=similar_count,
            similar_texts=similar_texts
        )
        
        explanations.append(f"[Duplicate Analysis] {duplicate_explanation}")
        scores.append(duplicate_score)
        
    except Exception as e:
        print(f"Error in duplicate detection: {e}")
        explanations.append("[Duplicate Analysis] Could not perform duplicate detection.")
        scores.append(0.0)
    
    # ============================================================
    # 2. PROMOTIONAL LANGUAGE DETECTION (Rule-based)
    # ============================================================
    try:
        manipulation_score, found_keywords = detect_promotional_language(
            description=full_text
        )
        
        manipulation_explanation = get_manipulation_explanation(
            manipulation_score=manipulation_score,
            found_keywords=found_keywords
        )
        
        explanations.append(f"[Promotional Language] {manipulation_explanation}")
        scores.append(manipulation_score)
        
    except Exception as e:
        print(f"Error in manipulation detection: {e}")
        explanations.append("[Promotional Language] Could not perform manipulation detection.")
        scores.append(0.0)
    
    # ============================================================
    # 3. TEXT LENGTH ANALYSIS
    # ============================================================
    try:
        length_score, length_explanation = analyze_text_length(description)
        
        if length_score > 0.2:  # Only add if significant
            explanations.append(f"[Text Length] {length_explanation}")
            scores.append(length_score)
        
    except Exception as e:
        print(f"Error in length analysis: {e}")
    
    # ============================================================
    # 4. COMBINE SCORES (Conservative approach: use maximum)
    # ============================================================
    # Using max ensures we don't dilute strong signals
    # If either duplicate OR manipulation is high, we flag it
    text_fraud_score = max(scores) if scores else 0.0
    
    # Add summary explanation
    if text_fraud_score > 0.7:
        summary = (
            f"⚠️ HIGH RISK: Text fraud score is {text_fraud_score:.2f}. "
            f"This listing shows strong indicators of fraudulent content."
        )
        explanations.insert(0, summary)
    elif text_fraud_score > 0.4:
        summary = (
            f"⚠️ MODERATE RISK: Text fraud score is {text_fraud_score:.2f}. "
            f"This listing shows some suspicious textual patterns."
        )
        explanations.insert(0, summary)
    else:
        summary = (
            f"✓ LOW RISK: Text fraud score is {text_fraud_score:.2f}. "
            f"No significant textual fraud indicators detected."
        )
        explanations.insert(0, summary)
    
    return text_fraud_score, explanations


def get_text_fraud_details(
    title: str,
    description: str
) -> dict:
    """
    Get detailed breakdown of text fraud analysis
    
    Args:
        title: Listing title
        description: Listing description
        
    Returns:
        dict: Detailed analysis with individual scores
    """
    full_text = f"{title}. {description}"
    
    # Get individual scores
    duplicate_score, similar_count, similar_texts = detect_duplicate_text(
        description=full_text,
        save_to_corpus_flag=False  # Don't save when getting details
    )
    
    manipulation_score, found_keywords = detect_promotional_language(full_text)
    length_score, length_explanation = analyze_text_length(description)
    
    # Combine
    final_score = max(duplicate_score, manipulation_score, length_score)
    
    return {
        "overall_score": final_score,
        "duplicate_detection": {
            "score": duplicate_score,
            "similar_count": similar_count,
            "method": "TF-IDF + Cosine Similarity"
        },
        "manipulation_detection": {
            "score": manipulation_score,
            "keywords_found": sum(len(kws) for kws in found_keywords.values()),
            "categories": {k: len(v) for k, v in found_keywords.items() if v},
            "method": "Rule-based Keyword Analysis"
        },
        "length_analysis": {
            "score": length_score,
            "word_count": len(description.split()),
            "char_count": len(description)
        }
    }
