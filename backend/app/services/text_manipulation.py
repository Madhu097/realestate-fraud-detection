"""
Text Manipulation Detection Service
Detects promotional/exaggerated language in listing descriptions
"""
import re
from typing import Tuple, List, Dict

# Comprehensive list of promotional/manipulative keywords
PROMOTIONAL_KEYWORDS = {
    # Luxury/Premium terms
    'luxury', 'premium', 'world-class', 'ultra-modern', 'lavish', 'opulent',
    'exquisite', 'prestigious', 'exclusive', 'elite', 'deluxe', 'magnificent',
    'spectacular', 'stunning', 'breathtaking', 'extraordinary', 'exceptional',
    
    # Urgency/Pressure terms
    'urgent sale', 'urgent', 'hurry', 'limited time', 'dont miss', "don't miss",
    'act now', 'last chance', 'going fast', 'wont last', "won't last",
    'grab now', 'book now', 'immediate', 'asap',
    
    # Superlatives
    'best deal', 'best price', 'lowest price', 'unbeatable', 'cheapest',
    'finest', 'greatest', 'ultimate', 'supreme', 'perfect', 'ideal',
    'amazing', 'incredible', 'unbelievable', 'fantastic', 'fabulous',
    
    # Dream/Emotion terms
    'dream home', 'dream property', 'paradise', 'heaven', 'bliss',
    'once in a lifetime', 'rare opportunity', 'golden opportunity',
    
    # Exaggeration
    'never before', 'one of a kind', 'unique opportunity', 'guaranteed',
    'absolutely', 'completely', 'totally', 'fully loaded', 'state of the art',
    
    # Investment/Money terms
    'steal', 'bargain', 'giveaway', 'hot deal', 'super deal', 'mega deal',
    'price reduced', 'must sell', 'distress sale', 'bank sale',
    
    # Comparison terms
    'better than', 'superior to', 'outperforms', 'beats all',
    
    # Vague promises
    'high returns', 'quick profit', 'easy money', 'risk-free',
    'no hidden charges', 'zero maintenance'
}

# Category weights for scoring
CATEGORY_WEIGHTS = {
    'urgency': 0.3,      # Urgency terms are highly manipulative
    'superlative': 0.25, # Exaggerated claims
    'luxury': 0.15,      # Luxury terms (less manipulative, more common)
    'emotion': 0.2,      # Emotional manipulation
    'money': 0.1         # Money-related pressure
}


def categorize_keywords() -> Dict[str, List[str]]:
    """Categorize promotional keywords by type"""
    return {
        'urgency': [
            'urgent sale', 'urgent', 'hurry', 'limited time', 'dont miss', "don't miss",
            'act now', 'last chance', 'going fast', 'wont last', "won't last",
            'grab now', 'book now', 'immediate', 'asap'
        ],
        'superlative': [
            'best deal', 'best price', 'lowest price', 'unbeatable', 'cheapest',
            'finest', 'greatest', 'ultimate', 'supreme', 'perfect', 'ideal',
            'amazing', 'incredible', 'unbelievable', 'fantastic', 'fabulous',
            'never before', 'one of a kind', 'unique opportunity'
        ],
        'luxury': [
            'luxury', 'premium', 'world-class', 'ultra-modern', 'lavish', 'opulent',
            'exquisite', 'prestigious', 'exclusive', 'elite', 'deluxe', 'magnificent',
            'spectacular', 'stunning', 'breathtaking', 'extraordinary', 'exceptional'
        ],
        'emotion': [
            'dream home', 'dream property', 'paradise', 'heaven', 'bliss',
            'once in a lifetime', 'rare opportunity', 'golden opportunity'
        ],
        'money': [
            'steal', 'bargain', 'giveaway', 'hot deal', 'super deal', 'mega deal',
            'price reduced', 'must sell', 'distress sale', 'bank sale',
            'high returns', 'quick profit', 'easy money', 'risk-free'
        ]
    }


def detect_promotional_language(description: str) -> Tuple[float, Dict[str, List[str]]]:
    """
    Detect promotional/manipulative language in description
    
    Args:
        description: Listing description text
        
    Returns:
        tuple: (manipulation_score, found_keywords_by_category)
            - manipulation_score (float): 0.0 to 1.0
            - found_keywords_by_category (dict): Keywords found in each category
    """
    # Convert to lowercase for matching
    text_lower = description.lower()
    
    # Get categorized keywords
    categories = categorize_keywords()
    
    # Find keywords in each category
    found_by_category = {}
    category_scores = {}
    
    for category, keywords in categories.items():
        found = []
        for keyword in keywords:
            # Use word boundaries for accurate matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                found.append(keyword)
        
        found_by_category[category] = found
        
        # Calculate category score
        if found:
            # Score based on: (number of keywords found / total keywords) * category weight
            # Plus bonus for multiple occurrences
            unique_count = len(found)
            total_count = sum(text_lower.count(kw) for kw in found)
            
            base_score = min(unique_count / len(keywords), 1.0)
            occurrence_bonus = min((total_count - unique_count) * 0.1, 0.3)
            
            category_scores[category] = (base_score + occurrence_bonus) * CATEGORY_WEIGHTS[category]
        else:
            category_scores[category] = 0.0
    
    # Calculate overall manipulation score
    # Sum of all category scores, capped at 1.0
    manipulation_score = min(sum(category_scores.values()), 1.0)
    
    return manipulation_score, found_by_category


def get_manipulation_explanation(
    manipulation_score: float,
    found_keywords: Dict[str, List[str]]
) -> str:
    """
    Generate human-readable explanation for manipulation detection
    
    Args:
        manipulation_score: Score from 0-1
        found_keywords: Keywords found by category
        
    Returns:
        str: Clear explanation
    """
    # Count total keywords
    total_keywords = sum(len(keywords) for keywords in found_keywords.values())
    
    if manipulation_score < 0.2:
        return (
            "The description uses professional language with minimal promotional content. "
            "No significant manipulation detected."
        )
    
    elif manipulation_score < 0.5:
        explanation = (
            f"The description contains {total_keywords} promotional keyword(s), "
            f"which is moderate but not highly suspicious. "
        )
        
        # Mention specific categories
        categories_found = [cat for cat, kws in found_keywords.items() if kws]
        if categories_found:
            explanation += f"Categories detected: {', '.join(categories_found)}. "
        
        return explanation
    
    else:
        # High manipulation score
        explanation = (
            f"The description contains excessive promotional language ({total_keywords} keywords found), "
            f"which is commonly associated with misleading advertisements. "
        )
        
        # List keywords by category
        details = []
        for category, keywords in found_keywords.items():
            if keywords:
                kw_list = ', '.join(f"'{kw}'" for kw in keywords[:5])  # Show max 5
                if len(keywords) > 5:
                    kw_list += f" and {len(keywords)-5} more"
                details.append(f"{category.title()}: {kw_list}")
        
        if details:
            explanation += "\n\nDetected keywords:\n" + "\n".join(details)
        
        return explanation


def analyze_text_length(description: str) -> Tuple[float, str]:
    """
    Analyze if description length is suspicious
    
    Args:
        description: Listing description
        
    Returns:
        tuple: (score, explanation)
    """
    length = len(description.strip())
    word_count = len(description.split())
    
    # Very short descriptions are suspicious
    if length < 50:
        return 0.6, f"Description is very short ({word_count} words), which may indicate low effort or fraud."
    
    # Very long descriptions might be copy-pasted
    elif length > 2000:
        return 0.3, f"Description is unusually long ({word_count} words), which may indicate copy-pasted content."
    
    # Normal length
    else:
        return 0.0, f"Description length is normal ({word_count} words)."
