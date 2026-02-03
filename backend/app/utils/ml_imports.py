"""
Conditional imports for optional ML dependencies
Makes the app work without pandas, numpy, sklearn, etc.
"""

# Try to import pandas, fallback to None
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    pd = None
    HAS_PANDAS = False

# Try to import numpy, fallback to None
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

# Try to import sklearn, fallback to None
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


def check_ml_available():
    """Check if ML libraries are available"""
    return HAS_PANDAS and HAS_NUMPY


def get_unavailable_message():
    """Get message about unavailable features"""
    missing = []
    if not HAS_PANDAS:
        missing.append("pandas")
    if not HAS_NUMPY:
        missing.append("numpy")
    if not HAS_SKLEARN:
        missing.append("scikit-learn")
    
    return f"ML features unavailable. Missing: {', '.join(missing)}. Upgrade to paid tier for full analysis."
