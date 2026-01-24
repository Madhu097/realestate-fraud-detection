"""
Image Fraud Detection Service
Detects duplicate/reused images using perceptual hashing
"""
from PIL import Image
import imagehash
import os
import json
from typing import Tuple, List, Dict

# Path to store image hashes
HASH_STORAGE_FILE = "app/data/image_hashes.json"


def load_image_hashes() -> List[Dict]:
    """Load existing image hashes from storage"""
    if not os.path.exists(HASH_STORAGE_FILE):
        return []
    
    try:
        with open(HASH_STORAGE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def save_image_hash(image_path: str, phash: str):
    """Save image hash to storage"""
    hashes = load_image_hashes()
    
    # Add new hash
    hashes.append({
        "image_path": image_path,
        "phash": phash
    })
    
    # Save to file
    os.makedirs(os.path.dirname(HASH_STORAGE_FILE), exist_ok=True)
    with open(HASH_STORAGE_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)


def compute_image_hash(image_path: str) -> str:
    """
    Compute perceptual hash (pHash) of an image
    
    Args:
        image_path: Path to image file
        
    Returns:
        str: Hexadecimal hash string
    """
    try:
        img = Image.open(image_path)
        # Compute perceptual hash (pHash)
        phash = imagehash.phash(img)
        return str(phash)
    except Exception as e:
        raise Exception(f"Error computing hash for {image_path}: {str(e)}")


def hamming_distance(hash1: str, hash2: str) -> int:
    """
    Calculate Hamming distance between two hashes
    
    Args:
        hash1: First hash string
        hash2: Second hash string
        
    Returns:
        int: Hamming distance (number of differing bits)
    """
    try:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return h1 - h2  # imagehash uses - operator for Hamming distance
    except:
        return 999  # Return high value if comparison fails


def detect_image_fraud(image_paths: List[str], save_hashes: bool = True) -> Tuple[float, int, str]:
    """
    Detect image fraud by comparing with previously uploaded images
    
    Args:
        image_paths: List of image file paths to analyze
        save_hashes: Whether to save hashes for future comparisons
        
    Returns:
        tuple: (fraud_score, duplicate_count, explanation)
            - fraud_score (float): 0.0 to 1.0
            - duplicate_count (int): Number of duplicate images found
            - explanation (str): Human-readable explanation
    """
    if not image_paths:
        return 0.0, 0, "No images provided for analysis."
    
    # Load existing hashes
    existing_hashes = load_image_hashes()
    
    # Compute hashes for new images
    new_hashes = []
    for img_path in image_paths:
        if not os.path.exists(img_path):
            continue
        
        try:
            phash = compute_image_hash(img_path)
            new_hashes.append({
                "image_path": img_path,
                "phash": phash
            })
        except Exception as e:
            print(f"Warning: Could not process {img_path}: {e}")
            continue
    
    if not new_hashes:
        return 0.0, 0, "Could not process any images."
    
    # Compare with existing hashes
    duplicate_count = 0
    similar_images = []
    
    # Hamming distance threshold
    # ≤ 8: Very similar (likely duplicate)
    # ≤ 15: Similar (possibly duplicate)
    DUPLICATE_THRESHOLD = 8
    
    for new_hash in new_hashes:
        for existing_hash in existing_hashes:
            distance = hamming_distance(new_hash["phash"], existing_hash["phash"])
            
            if distance <= DUPLICATE_THRESHOLD:
                duplicate_count += 1
                similar_images.append({
                    "new_image": os.path.basename(new_hash["image_path"]),
                    "existing_image": os.path.basename(existing_hash["image_path"]),
                    "similarity": f"{(1 - distance/64) * 100:.1f}%"  # Convert to percentage
                })
    
    # Save new hashes for future comparisons
    if save_hashes:
        for new_hash in new_hashes:
            save_image_hash(new_hash["image_path"], new_hash["phash"])
    
    # Calculate fraud score
    if duplicate_count == 0:
        fraud_score = 0.0
        explanation = (
            f"Analyzed {len(new_hashes)} image(s). "
            f"No duplicate or reused images detected. Images appear to be original."
        )
    elif duplicate_count == 1:
        fraud_score = 0.5
        explanation = (
            f"This image has been reused in 1 other listing, which is suspicious. "
            f"Reused images may indicate fraudulent listings."
        )
    else:
        # Multiple duplicates = high fraud score
        fraud_score = min(0.3 + (duplicate_count * 0.2), 1.0)
        explanation = (
            f"This image has been reused in {duplicate_count} other listings, which is highly suspicious. "
            f"Multiple reuses of the same image across listings is a strong indicator of fraud."
        )
    
    return fraud_score, duplicate_count, explanation
