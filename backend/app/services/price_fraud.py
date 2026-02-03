# Price Fraud Module - Finalized on Day 4
# Do not modify unless required for fusion

"""
Price Fraud Detection Service
Detects price anomalies using both Z-Score and IQR methods for statistical robustness

Methods:
1. Z-Score: Measures standard deviations from mean
2. IQR (Interquartile Range): Detects outliers using quartiles

Final score = max(z_score_normalized, iqr_score) for maximum sensitivity
"""
from app.utils.ml_imports import pd, HAS_PANDAS, get_unavailable_message


def detect_price_fraud(listing_price: float, locality: str, city: str, df=None):
    """
    Detect price fraud using combined Z-Score and IQR analysis
    
    Args:
        listing_price: Price of the listing to analyze
        locality: Locality/location name
        city: City name
        df: Real estate dataset (optional on free tier)
        
    Returns:
        tuple: (fraud_score, explanation)
            - fraud_score (float): 0.0 to 1.0, where 1.0 is definitely fraud
            - explanation (str): Human-readable explanation with statistics
    """
    # Check if pandas is available
    if not HAS_PANDAS or df is None:
        # Basic price validation without ML
        if listing_price < 100000:
            return 0.8, f"Price ₹{listing_price:,.0f} seems unusually low. {get_unavailable_message()}"
        elif listing_price > 100000000:
            return 0.7, f"Price ₹{listing_price:,.0f} seems unusually high. {get_unavailable_message()}"
        else:
            return 0.3, f"Price ₹{listing_price:,.0f} appears reasonable. {get_unavailable_message()}"
    
    # Filter dataset by city and locality (case-insensitive match)
    # Handle column names flexibly
    
    # 1. Filter by City first (if available in dataframe)
    if 'City' in df.columns:
        city_df = df[df["City"].str.lower() == city.lower()]
    elif 'city' in df.columns:
        city_df = df[df["city"].str.lower() == city.lower()]
    else:
        # Fallback if City column missing (Mumbai-only legacy data)
        city_df = df
        
    if len(city_df) == 0:
        return 0.0, (
            f"No data available for city '{city}'. "
            f"Cannot perform reliable price analysis."
        )

    # 2. Filter by Locality
    if 'Location' in df.columns:
        loc_col = 'Location'
    elif 'Locality' in df.columns:
        loc_col = 'Locality'
    else:
        loc_col = df.columns[2] # Fallback to 3rd column usually location
        
    locality_df = city_df[city_df[loc_col].str.lower() == locality.lower()]
    
    # EDGE CASE 1: Very small locality samples
    if len(locality_df) < 5:
        return 0.0, (
            f"Insufficient comparable listings in '{locality}' for reliable price analysis. "
            f"Only {len(locality_df)} properties found (minimum 5 required)."
        )
    
    # Extract price data
    prices = locality_df["Price"]
    
    # Compute basic statistics
    mean_price = prices.mean()
    median_price = prices.median()
    std_price = prices.std()
    
    # EDGE CASE 2: Zero variance (all prices identical)
    if std_price == 0 or pd.isna(std_price):
        if abs(listing_price - mean_price) < 0.01:
            return 0.0, (
                f"The listed price matches the standard price for '{locality}' "
                f"(₹{mean_price:,.0f})."
            )
        else:
            deviation_percent = abs(listing_price - mean_price) / mean_price * 100
            return 0.8, (
                f"All properties in '{locality}' are priced at ₹{mean_price:,.0f}, "
                f"but this listing is {deviation_percent:.1f}% different. "
                f"This is highly unusual."
            )
    
    # ============================================================
    # METHOD 1: Z-SCORE ANALYSIS
    # ============================================================
    z_score = abs(listing_price - mean_price) / std_price
    z_score_normalized = min(z_score / 3.0, 1.0)  # z > 3 is 99.7% anomaly
    
    # ============================================================
    # METHOD 2: IQR (INTERQUARTILE RANGE) ANALYSIS
    # ============================================================
    Q1 = prices.quantile(0.25)
    Q3 = prices.quantile(0.75)
    IQR = Q3 - Q1
    
    # IQR bounds (1.5 * IQR is standard for outlier detection)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Check if price is outside IQR bounds
    if listing_price < lower_bound:
        iqr_deviation = (lower_bound - listing_price) / IQR
        iqr_score = min(iqr_deviation / 2.0, 1.0)  # Normalize
        iqr_flag = "below_lower_bound"
    elif listing_price > upper_bound:
        iqr_deviation = (listing_price - upper_bound) / IQR
        iqr_score = min(iqr_deviation / 2.0, 1.0)  # Normalize
        iqr_flag = "above_upper_bound"
    else:
        iqr_score = 0.0
        iqr_flag = "within_bounds"
    
    # ============================================================
    # COMBINE BOTH METHODS (Take maximum for robustness)
    # ============================================================
    final_fraud_score = max(z_score_normalized, iqr_score)
    
    # ============================================================
    # GENERATE EXAMINER-APPROVED EXPLANATION
    # ============================================================
    deviation_percent = abs(listing_price - mean_price) / mean_price * 100
    
    # Determine if price is low or high
    if listing_price < mean_price:
        direction = "lower"
        comparison = "below"
    else:
        direction = "higher"
        comparison = "above"
    
    # Build detailed explanation based on fraud score
    if final_fraud_score > 0.6:
        # HIGH FRAUD RISK
        explanation = (
            f"The listed price of ₹{listing_price:,.0f} is {deviation_percent:.1f}% {comparison} "
            f"the average price of similar properties in '{locality}', which is statistically unusual. "
            f"Average: ₹{mean_price:,.0f}, Median: ₹{median_price:,.0f}. "
        )
        
        # Add IQR context if flagged
        if iqr_flag == "below_lower_bound":
            explanation += (
                f"This price falls below the normal range (₹{lower_bound:,.0f} - ₹{upper_bound:,.0f}) "
                f"and may indicate fraud or data entry error."
            )
        elif iqr_flag == "above_upper_bound":
            explanation += (
                f"This price exceeds the normal range (₹{lower_bound:,.0f} - ₹{upper_bound:,.0f}) "
                f"and may indicate price manipulation."
            )
        else:
            explanation += "This significant deviation warrants further investigation."
            
    elif final_fraud_score > 0.3:
        # MODERATE RISK
        explanation = (
            f"The listed price of ₹{listing_price:,.0f} is {deviation_percent:.1f}% {comparison} "
            f"the average for '{locality}'. "
            f"Average: ₹{mean_price:,.0f}, Median: ₹{median_price:,.0f}. "
            f"While not highly suspicious, this deviation is worth noting."
        )
        
    else:
        # LOW RISK (Normal)
        explanation = (
            f"The listed price of ₹{listing_price:,.0f} is within the normal range for '{locality}'. "
            f"Average: ₹{mean_price:,.0f}, Median: ₹{median_price:,.0f}. "
            f"Deviation: {deviation_percent:.1f}%. No price anomaly detected."
        )
    
    return final_fraud_score, explanation
