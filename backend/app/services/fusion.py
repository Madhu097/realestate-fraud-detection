"""
Fraud Fusion Engine
Combines multiple fraud detection signals into a single, explainable fraud decision

This module implements a weighted fusion strategy that is:
- Deterministic (same inputs always produce same outputs)
- Explainable (clear reasoning for every decision)
- Transparent (no black-box ML)
"""
from typing import List, Dict, Tuple, Optional


# ============================================================
# FUSION WEIGHTS (Carefully calibrated)
# ============================================================
# These weights reflect the relative importance and reliability
# of each fraud detection module

FUSION_WEIGHTS = {
    'price': 0.25,                    # 25% - Price is a strong fraud indicator
    'image': 0.20,                    # 20% - Image reuse is highly suspicious
    'text': 0.20,                     # 20% - Text manipulation is common
    'location': 0.15,                 # 15% - Internal location fraud detection
    'external_location': 0.15,        # 15% - External API location verification (NEW)
    'amenity': 0.05                   # 5% - Amenity claim verification (NEW)
}

# Fraud type threshold
FRAUD_TYPE_THRESHOLD = 0.6  # Only include fraud types with score > 0.6


def validate_fraud_score(score: float, module_name: str) -> float:
    """
    Validate and normalize fraud score
    
    Args:
        score: Fraud score to validate
        module_name: Name of the fraud module
        
    Returns:
        float: Validated score (0-1)
    """
    if score is None:
        return 0.0
    
    # Ensure score is in valid range
    if score < 0.0:
        print(f"Warning: {module_name} score {score} < 0, clamping to 0.0")
        return 0.0
    
    if score > 1.0:
        print(f"Warning: {module_name} score {score} > 1, clamping to 1.0")
        return 1.0
    
    return score


def weighted_fusion(
    price_score: float,
    image_score: float,
    text_score: float,
    location_score: float,
    external_location_score: float = 0.0,
    amenity_score: float = 0.0
) -> float:
    """
    Compute weighted fusion of fraud scores
    
    Formula:
    final_score = Σ(weight_i × score_i) for all modules
    
    This is a linear combination that preserves interpretability.
    Each module contributes proportionally to its weight.
    
    Args:
        price_score: Price fraud score (0-1)
        image_score: Image fraud score (0-1)
        text_score: Text fraud score (0-1)
        location_score: Location fraud score (0-1)
        external_location_score: External location verification score (0-1)
        amenity_score: Amenity verification score (0-1)
        
    Returns:
        float: Final fraud probability (0-1)
    """
    # Validate all scores
    price_score = validate_fraud_score(price_score, "Price")
    image_score = validate_fraud_score(image_score, "Image")
    text_score = validate_fraud_score(text_score, "Text")
    location_score = validate_fraud_score(location_score, "Location")
    external_location_score = validate_fraud_score(external_location_score, "External Location")
    amenity_score = validate_fraud_score(amenity_score, "Amenity")
    
    # Compute weighted sum
    final_score = (
        FUSION_WEIGHTS['price'] * price_score +
        FUSION_WEIGHTS['image'] * image_score +
        FUSION_WEIGHTS['text'] * text_score +
        FUSION_WEIGHTS['location'] * location_score +
        FUSION_WEIGHTS['external_location'] * external_location_score +
        FUSION_WEIGHTS['amenity'] * amenity_score
    )
    
    # Ensure result is in valid range (should always be true, but safety check)
    final_score = max(0.0, min(1.0, final_score))
    
    return final_score


def identify_fraud_types(
    price_score: float,
    image_score: float,
    text_score: float,
    location_score: float,
    external_location_score: float = 0.0,
    amenity_score: float = 0.0
) -> List[str]:
    """
    Identify which fraud types are present based on threshold
    
    A fraud type is included only if its score exceeds the threshold (0.6)
    This ensures we only flag high-confidence fraud signals
    
    Args:
        price_score: Price fraud score (0-1)
        image_score: Image fraud score (0-1)
        text_score: Text fraud score (0-1)
        location_score: Location fraud score (0-1)
        external_location_score: External location verification score (0-1)
        amenity_score: Amenity verification score (0-1)
        
    Returns:
        list: List of detected fraud types
    """
    fraud_types = []
    
    if price_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Price Fraud")
    
    if image_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Image Fraud")
    
    if text_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Text Fraud")
    
    if location_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Location Fraud")
    
    if external_location_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("External Location Fraud")
    
    if amenity_score > FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Amenity Fraud")
    
    return fraud_types


def aggregate_explanations(
    price_score: float,
    price_explanation: str,
    image_score: float,
    image_explanation: str,
    text_score: float,
    text_explanations: List[str],
    location_score: float,
    location_explanation: str,
    external_location_score: float = 0.0,
    external_location_explanation: str = "",
    amenity_score: float = 0.0,
    amenity_explanation: str = ""
) -> List[str]:
    """
    Aggregate explanations from all fraud modules
    
    Includes explanations from modules with significant fraud signals (score > 0.3)
    Orders explanations by fraud score (highest first)
    
    Args:
        price_score: Price fraud score
        price_explanation: Price fraud explanation
        image_score: Image fraud score
        image_explanation: Image fraud explanation
        text_score: Text fraud score
        text_explanations: Text fraud explanations (list)
        location_score: Location fraud score
        location_explanation: Location fraud explanation
        external_location_score: External location verification score
        external_location_explanation: External location explanation
        amenity_score: Amenity verification score
        amenity_explanation: Amenity explanation
        
    Returns:
        list: Aggregated explanations ordered by importance
    """
    # Collect all explanations with their scores
    all_explanations = []
    
    # Price
    if price_score > 0.3 and price_explanation:
        all_explanations.append({
            'score': price_score,
            'weight': FUSION_WEIGHTS['price'],
            'importance': price_score * FUSION_WEIGHTS['price'],
            'text': f"[Price] {price_explanation}"
        })
    
    # Image
    if image_score > 0.3 and image_explanation:
        all_explanations.append({
            'score': image_score,
            'weight': FUSION_WEIGHTS['image'],
            'importance': image_score * FUSION_WEIGHTS['image'],
            'text': f"[Image] {image_explanation}"
        })
    
    # Text (can have multiple explanations)
    if text_score > 0.3 and text_explanations:
        for text_exp in text_explanations:
            all_explanations.append({
                'score': text_score,
                'weight': FUSION_WEIGHTS['text'],
                'importance': text_score * FUSION_WEIGHTS['text'],
                'text': text_exp  # Text explanations already have [Text] prefix
            })
    
    # Location
    if location_score > 0.3 and location_explanation:
        all_explanations.append({
            'score': location_score,
            'weight': FUSION_WEIGHTS['location'],
            'importance': location_score * FUSION_WEIGHTS['location'],
            'text': f"[Location] {location_explanation}"
        })
    
    # External Location
    if external_location_score > 0.3 and external_location_explanation:
        all_explanations.append({
            'score': external_location_score,
            'weight': FUSION_WEIGHTS['external_location'],
            'importance': external_location_score * FUSION_WEIGHTS['external_location'],
            'text': f"[External Location] {external_location_explanation}"
        })
    
    # Amenity
    if amenity_score > 0.3 and amenity_explanation:
        all_explanations.append({
            'score': amenity_score,
            'weight': FUSION_WEIGHTS['amenity'],
            'importance': amenity_score * FUSION_WEIGHTS['amenity'],
            'text': f"[Amenity] {amenity_explanation}"
        })
    
    # Sort by importance (score × weight) - highest first
    all_explanations.sort(key=lambda x: x['importance'], reverse=True)
    
    # Extract just the text
    final_explanations = [exp['text'] for exp in all_explanations]
    
    return final_explanations


def generate_fusion_summary(
    final_fraud_probability: float,
    fraud_types: List[str],
    individual_scores: Dict[str, float]
) -> str:
    """
    Generate a summary explanation of the fusion decision
    
    Args:
        final_fraud_probability: Final fused fraud score
        fraud_types: List of detected fraud types
        individual_scores: Dictionary of individual module scores
        
    Returns:
        str: Summary explanation
    """
    # Determine risk level
    if final_fraud_probability >= 0.8:
        risk_level = "CRITICAL"
        risk_emoji = "🚨"
    elif final_fraud_probability >= 0.6:
        risk_level = "HIGH"
        risk_emoji = "⚠️"
    elif final_fraud_probability >= 0.4:
        risk_level = "MODERATE"
        risk_emoji = "⚠️"
    elif final_fraud_probability >= 0.2:
        risk_level = "LOW"
        risk_emoji = "ℹ️"
    else:
        risk_level = "MINIMAL"
        risk_emoji = "✓"
    
    # Build summary
    summary = f"{risk_emoji} {risk_level} RISK: Overall fraud probability is {final_fraud_probability:.1%}.\n"
    
    if fraud_types:
        summary += f"Detected fraud types: {', '.join(fraud_types)}.\n"
    else:
        summary += "No high-confidence fraud indicators detected.\n"
    
    # Add module breakdown
    summary += "\nModule Scores:\n"
    summary += f"  • Price: {individual_scores.get('price', 0):.1%} (weight: {FUSION_WEIGHTS['price']:.0%})\n"
    summary += f"  • Image: {individual_scores.get('image', 0):.1%} (weight: {FUSION_WEIGHTS['image']:.0%})\n"
    summary += f"  • Text: {individual_scores.get('text', 0):.1%} (weight: {FUSION_WEIGHTS['text']:.0%})\n"
    summary += f"  • Location: {individual_scores.get('location', 0):.1%} (weight: {FUSION_WEIGHTS['location']:.0%})\n"
    summary += f"  • External Location: {individual_scores.get('external_location', 0):.1%} (weight: {FUSION_WEIGHTS['external_location']:.0%})\n"
    summary += f"  • Amenity: {individual_scores.get('amenity', 0):.1%} (weight: {FUSION_WEIGHTS['amenity']:.0%})"
    
    return summary


def fuse_fraud_signals(
    price_score: float,
    price_explanation: str,
    image_score: float = 0.0,
    image_explanation: str = "",
    text_score: float = 0.0,
    text_explanations: List[str] = None,
    location_score: float = 0.0,
    location_explanation: str = "",
    external_location_score: float = 0.0,
    external_location_explanation: str = "",
    amenity_score: float = 0.0,
    amenity_explanation: str = ""
) -> Tuple[float, List[str], List[str]]:
    """
    Main fusion function - combines all fraud signals
    
    This is the primary entry point for the fusion engine.
    It orchestrates the entire fusion process:
    1. Validates inputs
    2. Computes weighted fusion
    3. Identifies fraud types
    4. Aggregates explanations
    5. Generates summary
    
    Args:
        price_score: Price fraud score (0-1)
        price_explanation: Price fraud explanation
        image_score: Image fraud score (0-1), optional
        image_explanation: Image fraud explanation, optional
        text_score: Text fraud score (0-1), optional
        text_explanations: Text fraud explanations (list), optional
        location_score: Location fraud score (0-1), optional
        location_explanation: Location fraud explanation, optional
        external_location_score: External location verification score (0-1), optional
        external_location_explanation: External location explanation, optional
        amenity_score: Amenity verification score (0-1), optional
        amenity_explanation: Amenity explanation, optional
        
    Returns:
        tuple: (final_fraud_probability, fraud_types, explanations)
            - final_fraud_probability (float): 0-1
            - fraud_types (list): List of detected fraud types
            - explanations (list): Aggregated explanations
    """
    # Handle None values
    if text_explanations is None:
        text_explanations = []
    
    # ============================================================
    # STEP 1: Compute weighted fusion
    # ============================================================
    final_fraud_probability = weighted_fusion(
        price_score=price_score,
        image_score=image_score,
        text_score=text_score,
        location_score=location_score,
        external_location_score=external_location_score,
        amenity_score=amenity_score
    )
    
    # ============================================================
    # STEP 2: Identify fraud types (threshold-based)
    # ============================================================
    fraud_types = identify_fraud_types(
        price_score=price_score,
        image_score=image_score,
        text_score=text_score,
        location_score=location_score,
        external_location_score=external_location_score,
        amenity_score=amenity_score
    )
    
    # ============================================================
    # STEP 3: Aggregate explanations (ordered by importance)
    # ============================================================
    explanations = aggregate_explanations(
        price_score=price_score,
        price_explanation=price_explanation,
        image_score=image_score,
        image_explanation=image_explanation,
        text_score=text_score,
        text_explanations=text_explanations,
        location_score=location_score,
        location_explanation=location_explanation,
        external_location_score=external_location_score,
        external_location_explanation=external_location_explanation,
        amenity_score=amenity_score,
        amenity_explanation=amenity_explanation
    )
    
    # ============================================================
    # STEP 4: Generate fusion summary
    # ============================================================
    individual_scores = {
        'price': price_score,
        'image': image_score,
        'text': text_score,
        'location': location_score,
        'external_location': external_location_score,
        'amenity': amenity_score
    }
    
    fusion_summary = generate_fusion_summary(
        final_fraud_probability=final_fraud_probability,
        fraud_types=fraud_types,
        individual_scores=individual_scores
    )
    
    # Add summary at the beginning
    explanations.insert(0, fusion_summary)
    
    return final_fraud_probability, fraud_types, explanations


def get_fusion_weights() -> Dict[str, float]:
    """
    Get current fusion weights
    
    Returns:
        dict: Fusion weights for each module
    """
    return FUSION_WEIGHTS.copy()


def explain_fusion_logic() -> str:
    """
    Explain the fusion logic in human-readable terms
    
    Returns:
        str: Explanation of fusion methodology
    """
    explanation = """
    FUSION ENGINE METHODOLOGY
    
    The fraud fusion engine combines signals from 4 independent fraud detection modules
    using a weighted linear combination:
    
    Final Score = (0.30 × Price) + (0.25 × Image) + (0.25 × Text) + (0.20 × Location)
    
    WEIGHT JUSTIFICATION:
    • Price (30%): Price anomalies are the strongest fraud indicator
    • Image (25%): Image reuse is highly suspicious and easy to verify
    • Text (25%): Text manipulation is common in fraudulent listings
    • Location (20%): Location fraud is detectable but less frequent
    
    FRAUD TYPE IDENTIFICATION:
    A fraud type is flagged only if its individual score exceeds 60%
    This ensures high-confidence fraud signals
    
    EXPLANATION AGGREGATION:
    Explanations are ordered by importance (score × weight)
    Only modules with score > 30% contribute explanations
    
    This approach is:
    ✓ Deterministic (same inputs → same outputs)
    ✓ Explainable (clear reasoning)
    ✓ Transparent (no black-box ML)
    ✓ Calibrated (weights based on fraud prevalence)
    """
    return explanation
