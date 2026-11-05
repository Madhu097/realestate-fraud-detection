"""
Text Manipulation and Phishing Detection Service
Detects high-pressure urgency keywords and advance-fee scam language
without falsely flagging standard residential descriptors.
"""
import re
from typing import Tuple, List, Dict

# Scammer pressure keywords
SCAM_CATEGORIES = {
    'urgency_pressure': [
        'urgent sale', 'must sell today', 'hurry up', 'limited time offer',
        'act now', 'dont miss', "don't miss", 'last chance', 'going fast',
        'grab now', 'book immediately', 'immediate cash', 'distress sale',
        'desperate sale', 'eviction sale'
    ],
    'advance_fee_phishing': [
        'wire transfer', 'western union', 'cash advance', 'advance payment',
        'token money', 'deposit now', 'owner abroad', 'transfer money before',
        'cannot visit', 'no questions asked', 'wire deposit', 'pay booking fee'
    ],
    'unrealistic_guarantee': [
        '100% guaranteed profit', 'zero risk investment', 'guaranteed double money',
        'miracle return', 'unbelievable giveaway'
    ]
}

def detect_promotional_language(description: str) -> Tuple[float, Dict[str, List[str]]]:
    """
    Detect genuine scam/phishing language in listing descriptions.
    """
    if not description:
        return 0.0, {}
        
    text_lower = description.lower()
    found_by_category = {}
    total_score = 0.0
    
    for category, keywords in SCAM_CATEGORIES.items():
        found = []
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                found.append(kw)
        found_by_category[category] = found
        
        if found:
            if category == 'advance_fee_phishing':
                total_score += 0.45 * len(found)
            elif category == 'urgency_pressure':
                total_score += 0.25 * len(found)
            elif category == 'unrealistic_guarantee':
                total_score += 0.30 * len(found)
                
    manipulation_score = min(total_score, 1.0)
    return round(manipulation_score, 2), found_by_category


def analyze_text_length(description: str) -> Tuple[float, str]:
    """Analyze if description text is too short or empty"""
    if not description or len(description.strip()) < 15:
        return 0.35, "Description is extremely brief, providing minimal verifiable detail."
    return 0.0, "Description length is adequate."


def get_manipulation_explanation(
    manipulation_score: float,
    found_keywords: Dict[str, List[str]]
) -> str:
    """Generate human-readable explanation for manipulation detection"""
    phishing = found_keywords.get('advance_fee_phishing', [])
    urgency = found_keywords.get('urgency_pressure', [])
    guarantees = found_keywords.get('unrealistic_guarantee', [])
    
    if phishing:
        return (
            f"🚨 CRITICAL PHISHING RISK: Description contains advance payment keywords: "
            f"'{', '.join(phishing)}'. Scammers use these to solicit unrecoverable deposits."
        )
    elif urgency:
        return (
            f"⚠️ HIGH URGENCY PRESSURE: Description contains artificial urgency triggers: "
            f"'{', '.join(urgency)}'. High-pressure language is often used to bypass buyer due-diligence."
        )
    elif guarantees:
        return (
            f"⚠️ UNREALISTIC CLAIMS: Found exaggerated guarantees: '{', '.join(guarantees)}'."
        )
    else:
        return "Description tone appears professional with no manipulative pressure detected."
