"""
Fraud Fusion Engine
Combines multiple fraud detection signals and the trained ML Hybrid Classifier
into a single, explainable, highly accurate fraud decision.
"""
from typing import List, Dict, Tuple, Optional

# Base Module Weights
FUSION_WEIGHTS = {
    'price': 0.35,                    # 35% - Price deviation / fair market valuation
    'text': 0.20,                     # 20% - Phishing / urgency / duplicate text
    'location': 0.20,                 # 20% - Geospatial accuracy
    'external_location': 0.10,        # 10% - External cross-reference
    'amenity': 0.05,                  # 5% - Amenity feasibility
    'image': 0.10                     # 10% - Image perceptual hash
}

FRAUD_TYPE_THRESHOLD = 0.50  # Only include fraud types with score >= 0.50


def validate_fraud_score(score: float, module_name: str) -> float:
    """Validate and clamp fraud score between 0.0 and 1.0"""
    if score is None:
        return 0.0
    return max(0.0, min(1.0, float(score)))


def weighted_fusion(
    price_score: float,
    image_score: float,
    text_score: float,
    location_score: float,
    external_location_score: float = 0.0,
    amenity_score: float = 0.0,
    ml_fraud_score: Optional[float] = None
) -> float:
    """
    Compute calibrated fusion of fraud scores and ML prediction.
    """
    price_score = validate_fraud_score(price_score, "Price")
    image_score = validate_fraud_score(image_score, "Image")
    text_score = validate_fraud_score(text_score, "Text")
    location_score = validate_fraud_score(location_score, "Location")
    external_location_score = validate_fraud_score(external_location_score, "External Location")
    amenity_score = validate_fraud_score(amenity_score, "Amenity")
    
    # Active weights (if image is 0.0 and not provided, renormalize)
    active_weights = dict(FUSION_WEIGHTS)
    if image_score == 0.0:
        active_weights['image'] = 0.0
        
    total_w = sum(active_weights.values())
    if total_w > 0:
        normalized_weights = {k: v / total_w for k, v in active_weights.items()}
    else:
        normalized_weights = FUSION_WEIGHTS

    modular_score = (
        normalized_weights['price'] * price_score +
        normalized_weights['image'] * image_score +
        normalized_weights['text'] * text_score +
        normalized_weights['location'] * location_score +
        normalized_weights['external_location'] * external_location_score +
        normalized_weights['amenity'] * amenity_score
    )
    
    # If ML Hybrid Classifier score is available, fuse with 50% ML + 50% Modular
    if ml_fraud_score is not None:
        ml_score = validate_fraud_score(ml_fraud_score, "ML Model")
        final_score = 0.50 * ml_score + 0.50 * modular_score
    else:
        final_score = modular_score

    # Check for extreme critical fraud signals (e.g. price discount > 75% or 50km location spoof)
    max_critical = max(price_score, location_score, text_score)
    if max_critical >= 0.85:
        final_score = max(final_score, max_critical * 0.90)

    return round(max(0.0, min(1.0, final_score)), 4)


def identify_fraud_types(
    price_score: float,
    image_score: float,
    text_score: float,
    location_score: float,
    external_location_score: float = 0.0,
    amenity_score: float = 0.0
) -> List[str]:
    """Identify which specific fraud types are active"""
    fraud_types = []
    if price_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Price Discrepancy / Deposit Bait")
    if text_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Phishing / Text Manipulation")
    if location_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Geospatial Mismatch")
    if external_location_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Unverified External Coordinates")
    if amenity_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Contradictory Amenity Claims")
    if image_score >= FRAUD_TYPE_THRESHOLD:
        fraud_types.append("Reused / Stolen Image")
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
    """Aggregate human-readable explanations sorted by importance"""
    explanations = []
    
    if price_explanation:
        explanations.append(f"[Price Valuation] {price_explanation}")
        
    if location_explanation:
        explanations.append(f"[Geospatial Verification] {location_explanation}")
        
    if text_explanations:
        for t in text_explanations:
            if t:
                explanations.append(t if t.startswith("[") else f"[Text Analysis] {t}")
                
    if external_location_score > 0.3 and external_location_explanation:
        explanations.append(f"[External Geocoding] {external_location_explanation}")
        
    if amenity_score > 0.3 and amenity_explanation:
        explanations.append(f"[Amenity Verification] {amenity_explanation}")
        
    if image_score > 0.3 and image_explanation:
        explanations.append(f"[Image Audit] {image_explanation}")
        
    return explanations


def generate_fusion_summary(
    final_fraud_probability: float,
    fraud_types: List[str],
    individual_scores: Dict[str, float]
) -> str:
    """Generate executive summary of the fraud analysis"""
    if final_fraud_probability >= 0.65:
        risk_level = "CRITICAL / HIGH RISK OF FRAUD"
        risk_emoji = "🚨"
        verdict = (
            f"{risk_emoji} {risk_level} (Fraud Probability: {final_fraud_probability:.1%}). "
            f"Active Warning Flags: {', '.join(fraud_types) if fraud_types else 'Multiple anomalous signals'}. "
            f"Prospective buyers/renters are strongly cautioned not to make advance deposits without in-person physical inspection."
        )
    elif final_fraud_probability >= 0.35:
        risk_level = "MODERATE RISK / EXERCISE CAUTION"
        risk_emoji = "⚠️"
        verdict = (
            f"{risk_emoji} {risk_level} (Fraud Probability: {final_fraud_probability:.1%}). "
            f"Some metrics deviate from standard market ranges. Review the detailed findings below before proceeding."
        )
    else:
        risk_level = "VERIFIED REAL LISTING / LOW RISK"
        risk_emoji = "✅"
        verdict = (
            f"{risk_emoji} {risk_level} (Authenticity Confidence: {(1.0 - final_fraud_probability):.1%}). "
            f"The listing price, floor area, price-per-sqft, and geospatial coordinates align with authentic real estate benchmarks."
        )
        
    return verdict


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
    amenity_explanation: str = "",
    ml_fraud_score: Optional[float] = None
) -> Tuple[float, List[str], List[str]]:
    """
    Main fusion function - orchestrates modular signals and ML prediction.
    """
    if text_explanations is None:
        text_explanations = []
        
    final_fraud_probability = weighted_fusion(
        price_score=price_score,
        image_score=image_score,
        text_score=text_score,
        location_score=location_score,
        external_location_score=external_location_score,
        amenity_score=amenity_score,
        ml_fraud_score=ml_fraud_score
    )
    
    fraud_types = identify_fraud_types(
        price_score=price_score,
        image_score=image_score,
        text_score=text_score,
        location_score=location_score,
        external_location_score=external_location_score,
        amenity_score=amenity_score
    )
    
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
    
    individual_scores = {
        'price': price_score,
        'image': image_score,
        'text': text_score,
        'location': location_score,
        'external_location': external_location_score,
        'amenity': amenity_score
    }
    
    summary = generate_fusion_summary(
        final_fraud_probability=final_fraud_probability,
        fraud_types=fraud_types,
        individual_scores=individual_scores
    )
    
    explanations.insert(0, summary)
    
    return final_fraud_probability, fraud_types, explanations


def get_fusion_weights() -> Dict[str, float]:
    """Get active fusion weights"""
    return FUSION_WEIGHTS.copy()
