"""
Test Script for Fraud Prediction Accuracy with UTF-8 support
"""
import sys
import os
from pathlib import Path
import asyncio

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.routers.analyze import analyze_listing, AnalyzeRequest, ListingData

async def run_tests():
    print("=" * 65)
    print("TEST 1: Legitimate Authentic Property")
    print("=" * 65)
    req1 = AnalyzeRequest(listing_data=ListingData(
        title="Spacious 2BHK Apartment in Banjara Hills",
        description="Beautiful well-ventilated 2BHK apartment with covered car parking, lift, power backup, and round-the-clock security. Clean title deed ready for registration.",
        price=9500000, # 95 Lakhs for 1100 sqft in Banjara Hills (~8600/sqft)
        area_sqft=1100,
        city="Hyderabad",
        locality="Banjara Hills",
        latitude=17.4239,
        longitude=78.4738
    ))
    res1 = await analyze_listing(req1)
    print(f"Prediction Fraud Probability: {res1.fraud_probability:.2%}")
    print(f"Detected Fraud Types: {res1.fraud_types}")
    print(f"Module Scores: {res1.module_scores}")
    print(f"Summary: {res1.explanations[0]}")
    print(f"ML Intelligence: {res1.explanations[1]}")
    print(f"Price note: {res1.explanations[2]}")
    assert res1.fraud_probability < 0.35, f"Expected low risk, got {res1.fraud_probability}"
    print(">> TEST 1 PASSED: Correctly predicted as REAL / LOW RISK!\n")

    print("=" * 65)
    print("TEST 2: Clear Advance-Fee Deposit Scam (Bait-and-Switch)")
    print("=" * 65)
    req2 = AnalyzeRequest(listing_data=ListingData(
        title="Ultra Luxury 3BHK Penthouse in Banjara Hills Urgent Sale",
        description="Distress emergency sale! Owner relocated abroad immediately. Hurry up! Wire transfer token money and advance deposit required before in-person viewing.",
        price=800000, # Only 8 Lakhs for 2200 sqft luxury flat in Banjara Hills! (Scam)
        area_sqft=2200,
        city="Hyderabad",
        locality="Banjara Hills",
        latitude=17.4239,
        longitude=78.4738
    ))
    res2 = await analyze_listing(req2)
    print(f"Prediction Fraud Probability: {res2.fraud_probability:.2%}")
    print(f"Detected Fraud Types: {res2.fraud_types}")
    print(f"Module Scores: {res2.module_scores}")
    print(f"Summary: {res2.explanations[0]}")
    print(f"ML Intelligence: {res2.explanations[1]}")
    assert res2.fraud_probability >= 0.65, f"Expected high risk, got {res2.fraud_probability}"
    print(">> TEST 2 PASSED: Correctly predicted as HIGH FRAUD RISK!\n")

    print("=" * 65)
    print("TEST 3: Location Spoofing / Phantom Listing")
    print("=" * 65)
    req3 = AnalyzeRequest(listing_data=ListingData(
        title="2BHK Apartment in Andheri West",
        description="Spacious 2BHK flat near metro and link road.",
        price=16000000, # 1.6 Cr for 900 sqft in Andheri West is fair price
        area_sqft=900,
        city="Mumbai",
        locality="Andheri West",
        latitude=18.5204, # Pune coordinates (150 km away!)
        longitude=73.8567
    ))
    res3 = await analyze_listing(req3)
    print(f"Prediction Fraud Probability: {res3.fraud_probability:.2%}")
    print(f"Detected Fraud Types: {res3.fraud_types}")
    print(f"Module Scores: {res3.module_scores}")
    print(f"Summary: {res3.explanations[0]}")
    assert "Geospatial Mismatch" in res3.fraud_types or res3.module_scores.get("Location", 0) > 0.6, "Expected location fraud detected"
    print(">> TEST 3 PASSED: Correctly flagged Geospatial Mismatch!\n")

    print("=" * 65)
    print("ALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(run_tests())
