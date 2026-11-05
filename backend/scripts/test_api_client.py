import sys
import json
import time
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.routers.analyze import analyze_listing, AnalyzeRequest, ListingData

def safe_print(*args):
    text = " ".join(str(a) for a in args)
    print(text.encode('ascii', 'backslashreplace').decode('ascii'))

safe_print("=" * 60)
safe_print("TEST 1: Legitimate Property Submission")
safe_print("=" * 60)
req1 = AnalyzeRequest(listing_data=ListingData(
    title="Spacious 2BHK Apartment in Banjara Hills",
    description="Beautiful well-ventilated 2BHK apartment with covered car parking, lift, power backup, and round-the-clock security. Clean title deed ready for registration.",
    price=9500000,
    area_sqft=1100,
    city="Hyderabad",
    locality="Banjara Hills",
    latitude=17.4239,
    longitude=78.4738
))
t0 = time.time()
res1 = analyze_listing(req1)
safe_print(f"Executed in {time.time()-t0:.3f}s")
safe_print("Fraud Probability:", res1.fraud_probability)
safe_print("Fraud Types:", res1.fraud_types)
safe_print("Module Scores:", res1.module_scores)
safe_print("Summary:", res1.explanations[0])
safe_print("ML Intelligence:", res1.explanations[1])
assert res1.fraud_probability < 0.35
safe_print(">> PASSED AUTHENTIC LISTING TEST!\n")

safe_print("=" * 60)
safe_print("TEST 2: Clear Advance-Fee Scam (Extreme Discount / Deposit Bait)")
safe_print("=" * 60)
req2 = AnalyzeRequest(listing_data=ListingData(
    title="Ultra Luxury 3BHK Penthouse in Banjara Hills Urgent Sale",
    description="Distress emergency sale! Owner relocated abroad immediately. Hurry up! Wire transfer token money and advance deposit required before in-person viewing.",
    price=800000, # Only 8 Lakhs for 2200 sqft in Banjara Hills!
    area_sqft=2200,
    city="Hyderabad",
    locality="Banjara Hills",
    latitude=17.4239,
    longitude=78.4738
))
t0 = time.time()
res2 = analyze_listing(req2)
safe_print(f"Executed in {time.time()-t0:.3f}s")
safe_print("Fraud Probability:", res2.fraud_probability)
safe_print("Fraud Types:", res2.fraud_types)
safe_print("Module Scores:", res2.module_scores)
safe_print("Summary:", res2.explanations[0])
assert res2.fraud_probability >= 0.65
safe_print(">> PASSED ADVANCE-FEE SCAM TEST!\n")

safe_print("=" * 60)
safe_print("TEST 3: Location Spoofing Scam")
safe_print("=" * 60)
req3 = AnalyzeRequest(listing_data=ListingData(
    title="2BHK Apartment in Andheri West",
    description="Spacious 2BHK flat near metro and link road.",
    price=16000000,
    area_sqft=900,
    city="Mumbai",
    locality="Andheri West",
    latitude=18.5204, # 150 km away in Pune
    longitude=73.8567
))
t0 = time.time()
res3 = analyze_listing(req3)
safe_print(f"Executed in {time.time()-t0:.3f}s")
safe_print("Fraud Probability:", res3.fraud_probability)
safe_print("Fraud Types:", res3.fraud_types)
safe_print("Module Scores:", res3.module_scores)
safe_print("Summary:", res3.explanations[0])
assert res3.module_scores.get("Location", 0) >= 0.60
safe_print(">> PASSED LOCATION SPOOFING TEST!\n")

safe_print("=" * 60)
safe_print("ALL 3 TESTS PASSED WITH ACCURATE RESULTS AND TRAINED ML MODELS!")
safe_print("=" * 60)
