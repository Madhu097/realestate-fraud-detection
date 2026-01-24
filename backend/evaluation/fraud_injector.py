"""
Synthetic Fraud Injection Module

This module creates synthetic fraudulent listings by injecting various fraud patterns
into normal listings. This is used for evaluation purposes only.

Fraud Types Injected:
1. Price Fraud - Abnormally low/high prices
2. Text Fraud - Suspicious keywords, manipulation patterns
3. Location Fraud - Coordinate mismatches
4. Image Fraud - (Placeholder for future implementation)
"""
import pandas as pd
import numpy as np
import random
from typing import Dict, List, Tuple


# ============================================================
# FRAUD INJECTION PATTERNS
# ============================================================

# Text fraud patterns
URGENCY_KEYWORDS = [
    "urgent", "hurry", "limited time", "act now", "don't miss",
    "last chance", "today only", "immediate", "quick sale"
]

SCAM_KEYWORDS = [
    "guaranteed", "risk-free", "100% safe", "no questions asked",
    "cash only", "wire transfer", "advance payment", "deposit now"
]

EXAGGERATION_KEYWORDS = [
    "luxury", "premium", "exclusive", "world-class", "best",
    "amazing", "incredible", "unbelievable", "perfect"
]


def inject_price_fraud(row: pd.Series, fraud_type: str = "underpriced") -> pd.Series:
    """
    Inject price fraud into a listing
    
    Args:
        row: Original listing data
        fraud_type: Type of price fraud ("underpriced" or "overpriced")
        
    Returns:
        Modified listing with price fraud
    """
    row = row.copy()
    
    if fraud_type == "underpriced":
        # Make price 40-70% below normal
        reduction_factor = random.uniform(0.3, 0.6)
        row['price'] = row['price'] * reduction_factor
        row['fraud_label'] = 1
        row['fraud_type'] = 'Price Fraud'
        row['fraud_details'] = f'Price reduced by {(1-reduction_factor)*100:.0f}%'
        
    elif fraud_type == "overpriced":
        # Make price 50-100% above normal
        increase_factor = random.uniform(1.5, 2.0)
        row['price'] = row['price'] * increase_factor
        row['fraud_label'] = 1
        row['fraud_type'] = 'Price Fraud'
        row['fraud_details'] = f'Price increased by {(increase_factor-1)*100:.0f}%'
    
    return row


def inject_text_fraud(row: pd.Series, fraud_type: str = "urgency") -> pd.Series:
    """
    Inject text fraud into a listing
    
    Args:
        row: Original listing data
        fraud_type: Type of text fraud ("urgency", "scam", "exaggeration")
        
    Returns:
        Modified listing with text fraud
    """
    row = row.copy()
    
    if fraud_type == "urgency":
        # Add urgency keywords
        keywords = random.sample(URGENCY_KEYWORDS, k=random.randint(2, 4))
        row['description'] = f"{' '.join(keywords).upper()}! {row['description']}"
        row['fraud_label'] = 1
        row['fraud_type'] = 'Text Fraud'
        row['fraud_details'] = f'Urgency keywords: {", ".join(keywords)}'
        
    elif fraud_type == "scam":
        # Add scam keywords
        keywords = random.sample(SCAM_KEYWORDS, k=random.randint(2, 3))
        row['description'] = f"{row['description']} {' '.join(keywords)}."
        row['fraud_label'] = 1
        row['fraud_type'] = 'Text Fraud'
        row['fraud_details'] = f'Scam keywords: {", ".join(keywords)}'
        
    elif fraud_type == "exaggeration":
        # Add excessive exaggeration
        keywords = random.sample(EXAGGERATION_KEYWORDS, k=random.randint(4, 6))
        row['title'] = f"{' '.join(keywords[:3]).upper()} {row['title']}"
        row['description'] = f"{' '.join(keywords[3:]).upper()}! {row['description']}"
        row['fraud_label'] = 1
        row['fraud_type'] = 'Text Fraud'
        row['fraud_details'] = f'Exaggeration keywords: {", ".join(keywords)}'
    
    return row


def inject_location_fraud(row: pd.Series, fraud_type: str = "coordinate_mismatch") -> pd.Series:
    """
    Inject location fraud into a listing
    
    Args:
        row: Original listing data
        fraud_type: Type of location fraud
        
    Returns:
        Modified listing with location fraud
    """
    row = row.copy()
    
    if fraud_type == "coordinate_mismatch":
        # Shift coordinates significantly (0.5-2 degrees)
        lat_shift = random.uniform(0.5, 2.0) * random.choice([-1, 1])
        lon_shift = random.uniform(0.5, 2.0) * random.choice([-1, 1])
        
        original_lat = row['latitude']
        original_lon = row['longitude']
        
        row['latitude'] = row['latitude'] + lat_shift
        row['longitude'] = row['longitude'] + lon_shift
        
        # Ensure coordinates stay in valid range
        row['latitude'] = max(-90, min(90, row['latitude']))
        row['longitude'] = max(-180, min(180, row['longitude']))
        
        row['fraud_label'] = 1
        row['fraud_type'] = 'Location Fraud'
        row['fraud_details'] = f'Coordinates shifted by ({lat_shift:.2f}, {lon_shift:.2f})'
    
    return row


def inject_multi_fraud(row: pd.Series, fraud_types: List[str]) -> pd.Series:
    """
    Inject multiple fraud types into a single listing
    
    Args:
        row: Original listing data
        fraud_types: List of fraud types to inject
        
    Returns:
        Modified listing with multiple fraud types
    """
    row = row.copy()
    fraud_details_list = []
    
    for fraud_type in fraud_types:
        if fraud_type.startswith("price_"):
            row = inject_price_fraud(row, fraud_type.replace("price_", ""))
        elif fraud_type.startswith("text_"):
            row = inject_text_fraud(row, fraud_type.replace("text_", ""))
        elif fraud_type.startswith("location_"):
            row = inject_location_fraud(row, fraud_type.replace("location_", ""))
        
        if 'fraud_details' in row:
            fraud_details_list.append(row['fraud_details'])
    
    row['fraud_type'] = 'Multi-Fraud'
    row['fraud_details'] = ' | '.join(fraud_details_list)
    
    return row


def normalize_dataset_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dataset columns to match expected schema
    
    Args:
        df: Original dataset with various column names
        
    Returns:
        DataFrame with normalized columns
    """
    df = df.copy()
    
    # Map actual columns to expected columns
    column_mapping = {
        'Price': 'price',
        'Area': 'area_sqft',
        'Location': 'locality',
        'No. of Bedrooms': 'bedrooms'
    }
    
    # Rename columns
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]
    
    # Create missing required fields with defaults
    if 'title' not in df.columns:
        # Generate title from available data
        if 'bedrooms' in df.columns:
            df['title'] = df.apply(
                lambda row: f"{int(row['bedrooms']) if pd.notna(row.get('bedrooms')) else 2}BHK Property in {row.get('locality', 'Prime Location')}",
                axis=1
            )
        else:
            df['title'] = df.apply(
                lambda row: f"Property in {row.get('locality', 'Prime Location')}",
                axis=1
            )
    
    if 'description' not in df.columns:
        # Generate description from available data
        df['description'] = df.apply(
            lambda row: f"Beautiful property with {int(row.get('area_sqft', 1000))} sqft area in {row.get('locality', 'prime location')}. Well-maintained and ready to move in.",
            axis=1
        )
    
    if 'city' not in df.columns:
        df['city'] = 'Mumbai'  # Default city
    
    # Generate coordinates if not present
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        # Use Mumbai coordinates with random offset
        base_lat, base_lon = 19.0760, 72.8777
        df['latitude'] = base_lat + np.random.uniform(-0.5, 0.5, len(df))
        df['longitude'] = base_lon + np.random.uniform(-0.5, 0.5, len(df))
    
    return df


def create_synthetic_fraud_dataset(
    df: pd.DataFrame,
    num_fraudulent: int = 200,
    fraud_distribution: Dict[str, float] = None
) -> pd.DataFrame:
    """
    Create a labeled dataset with synthetic fraudulent listings
    
    Args:
        df: Original dataset (normal listings)
        num_fraudulent: Number of fraudulent listings to create
        fraud_distribution: Distribution of fraud types (if None, uses default)
        
    Returns:
        DataFrame with both normal and fraudulent listings, labeled
    """
    # Normalize dataset columns first
    df = normalize_dataset_columns(df)
    
    if fraud_distribution is None:
        # Default distribution
        fraud_distribution = {
            'price_underpriced': 0.25,
            'price_overpriced': 0.15,
            'text_urgency': 0.20,
            'text_scam': 0.15,
            'text_exaggeration': 0.10,
            'location_coordinate_mismatch': 0.10,
            'multi_fraud': 0.05
        }
    
    # Validate distribution sums to 1.0
    total = sum(fraud_distribution.values())
    if not (0.99 <= total <= 1.01):
        raise ValueError(f"Fraud distribution must sum to 1.0 (got {total})")
    
    # Sample normal listings to inject fraud into
    sample_size = min(num_fraudulent, len(df))
    sampled_listings = df.sample(n=sample_size, random_state=42).copy()
    
    # Calculate number of each fraud type
    fraud_counts = {
        fraud_type: int(sample_size * proportion)
        for fraud_type, proportion in fraud_distribution.items()
    }
    
    # Adjust for rounding errors
    total_assigned = sum(fraud_counts.values())
    if total_assigned < sample_size:
        # Add remaining to most common type
        most_common = max(fraud_counts, key=fraud_counts.get)
        fraud_counts[most_common] += (sample_size - total_assigned)
    
    # Create fraudulent listings
    fraudulent_listings = []
    start_idx = 0
    
    for fraud_type, count in fraud_counts.items():
        if count == 0:
            continue
            
        end_idx = start_idx + count
        subset = sampled_listings.iloc[start_idx:end_idx].copy()
        
        if fraud_type == 'multi_fraud':
            # Inject 2-3 fraud types
            modified_rows = []
            for idx in range(len(subset)):
                fraud_types = random.sample([
                    'price_underpriced', 'text_urgency', 'text_scam', 
                    'location_coordinate_mismatch'
                ], k=random.randint(2, 3))
                modified_row = inject_multi_fraud(subset.iloc[idx].copy(), fraud_types)
                modified_rows.append(modified_row)
            subset = pd.DataFrame(modified_rows)
        else:
            # Inject single fraud type
            if fraud_type.startswith('price_'):
                subset = subset.apply(
                    lambda row: inject_price_fraud(row, fraud_type.replace('price_', '')),
                    axis=1
                )
            elif fraud_type.startswith('text_'):
                subset = subset.apply(
                    lambda row: inject_text_fraud(row, fraud_type.replace('text_', '')),
                    axis=1
                )
            elif fraud_type.startswith('location_'):
                subset = subset.apply(
                    lambda row: inject_location_fraud(row, fraud_type.replace('location_', '')),
                    axis=1
                )
        
        fraudulent_listings.append(subset)
        start_idx = end_idx
    
    # Combine all fraudulent listings
    fraudulent_df = pd.concat(fraudulent_listings, ignore_index=True)
    
    # Create normal listings dataset (labeled as non-fraudulent)
    normal_df = df.sample(n=len(fraudulent_df), random_state=43).copy()  # Different seed to avoid overlap
    normal_df['fraud_label'] = 0
    normal_df['fraud_type'] = 'Normal'
    normal_df['fraud_details'] = 'No fraud detected'
    
    # Combine normal and fraudulent
    evaluation_dataset = pd.concat([normal_df, fraudulent_df], ignore_index=True)
    
    # Shuffle the dataset
    evaluation_dataset = evaluation_dataset.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return evaluation_dataset


def get_fraud_statistics(df: pd.DataFrame) -> Dict:
    """
    Get statistics about the fraud dataset
    
    Args:
        df: Labeled fraud dataset
        
    Returns:
        Dictionary with fraud statistics
    """
    stats = {
        'total_listings': len(df),
        'normal_listings': len(df[df['fraud_label'] == 0]),
        'fraudulent_listings': len(df[df['fraud_label'] == 1]),
        'fraud_percentage': (len(df[df['fraud_label'] == 1]) / len(df)) * 100,
        'fraud_type_distribution': df[df['fraud_label'] == 1]['fraud_type'].value_counts().to_dict()
    }
    
    return stats


if __name__ == "__main__":
    # Test fraud injection
    print("Testing fraud injection module...")
    
    # Create sample listing with correct column names
    sample_listing = pd.Series({
        'title': 'Beautiful 3BHK Apartment',
        'description': 'Spacious apartment with modern amenities',
        'price': 5000000,
        'area_sqft': 1500,
        'city': 'Mumbai',
        'locality': 'Andheri West',
        'latitude': 19.1334,
        'longitude': 72.8291
    })
    
    print("\n=== Original Listing ===")
    print(f"Title: {sample_listing['title']}")
    print(f"Price: {sample_listing['price']}")
    print(f"Description: {sample_listing['description']}")
    
    # Test price fraud
    print("\n=== Price Fraud (Underpriced) ===")
    price_fraud = inject_price_fraud(sample_listing.copy(), "underpriced")
    print(f"New Price: {price_fraud['price']}")
    print(f"Fraud Details: {price_fraud['fraud_details']}")
    
    # Test text fraud
    print("\n=== Text Fraud (Urgency) ===")
    text_fraud = inject_text_fraud(sample_listing.copy(), "urgency")
    print(f"New Description: {text_fraud['description']}")
    print(f"Fraud Details: {text_fraud['fraud_details']}")
    
    # Test location fraud
    print("\n=== Location Fraud ===")
    location_fraud = inject_location_fraud(sample_listing.copy(), "coordinate_mismatch")
    print(f"Original Coords: ({sample_listing['latitude']}, {sample_listing['longitude']})")
    print(f"New Coords: ({location_fraud['latitude']}, {location_fraud['longitude']})")
    print(f"Fraud Details: {location_fraud['fraud_details']}")
    
    print("\n✅ Fraud injection module test complete!")

