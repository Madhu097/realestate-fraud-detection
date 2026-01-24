# Fraud Detection System - Test Cases & Demo Scenarios

## Overview

This document provides structured test cases for live demo and evaluation of the Truth in Listings fraud detection system.

**Test Date**: January 20, 2026  
**System Version**: 2.1.0  
**Tester**: QA Engineer  

---

## Test Case Categories

1. **Normal Listings** (3 cases) - Should show LOW fraud probability
2. **Price Fraud** (2 cases) - Should detect price anomalies
3. **Text Fraud** (2 cases) - Should detect suspicious text patterns
4. **Location Fraud** (1 case) - Should detect coordinate mismatches
5. **Multi-Fraud** (1 case) - Should detect multiple fraud types

**Total**: 9 Test Cases

---

## 🟢 NORMAL LISTINGS (Expected: Low Fraud Probability < 0.3)

### Test Case N1: Standard 2BHK Apartment

**Category**: Normal Listing  
**Expected Fraud Probability**: 0.05 - 0.20  
**Expected Fraud Types**: None  

**Input Data**:
```json
{
  "title": "Spacious 2BHK Apartment in Prime Location",
  "description": "Well-maintained 2BHK apartment with 2 bathrooms, modular kitchen, and covered parking. Located in a peaceful residential area with good connectivity to schools and hospitals.",
  "price": 4500000,
  "area_sqft": 1100,
  "city": "Mumbai",
  "locality": "Andheri West",
  "latitude": 19.1334,
  "longitude": 72.8291
}
```

**Expected Output**:
- Fraud Probability: ~0.10 - 0.20
- Fraud Types: [] (empty)
- Price Score: < 0.3
- Text Score: < 0.3
- Location Score: < 0.3
- Explanations: "Price is within normal range for locality", "No suspicious text patterns detected"

**Test Steps**:
1. Enter all fields in the form
2. Click "Initialize Fraud Detection Sequence"
3. Wait for analysis (2-5 seconds)
4. Verify fraud probability is LOW (green indicator)
5. Verify no fraud types are flagged
6. Verify all module scores are low

---

### Test Case N2: Luxury 3BHK Penthouse

**Category**: Normal Listing  
**Expected Fraud Probability**: 0.10 - 0.25  
**Expected Fraud Types**: None  

**Input Data**:
```json
{
  "title": "Premium 3BHK Penthouse with Panoramic Views",
  "description": "Luxurious penthouse featuring 3 spacious bedrooms, 3 bathrooms, imported modular kitchen, private terrace, and dedicated parking. Building amenities include swimming pool, gym, and 24/7 security.",
  "price": 12500000,
  "area_sqft": 2200,
  "city": "Mumbai",
  "locality": "Bandra West",
  "latitude": 19.0596,
  "longitude": 72.8295
}
```

**Expected Output**:
- Fraud Probability: ~0.15 - 0.25
- Fraud Types: [] (empty)
- Price Score: < 0.4
- Text Score: < 0.3
- Location Score: < 0.3
- Explanations: "Price appropriate for luxury segment", "Property description is detailed and professional"

**Test Steps**:
1. Enter all fields in the form
2. Submit for analysis
3. Verify LOW fraud probability
4. Verify professional listing is not flagged
5. Check that "luxury" keywords don't trigger false positives

---

### Test Case N3: Budget 1BHK Flat

**Category**: Normal Listing  
**Expected Fraud Probability**: 0.05 - 0.20  
**Expected Fraud Types**: None  

**Input Data**:
```json
{
  "title": "Affordable 1BHK Flat for First-Time Buyers",
  "description": "Compact 1BHK flat ideal for bachelors or small families. Includes basic amenities, close to railway station and market. Ready to move in condition.",
  "price": 2800000,
  "area_sqft": 550,
  "city": "Mumbai",
  "locality": "Malad East",
  "latitude": 19.1868,
  "longitude": 72.8493
}
```

**Expected Output**:
- Fraud Probability: ~0.10 - 0.20
- Fraud Types: [] (empty)
- Price Score: < 0.3
- Text Score: < 0.3
- Location Score: < 0.3
- Explanations: "Price consistent with area and size", "Straightforward property description"

**Test Steps**:
1. Enter all fields
2. Submit for analysis
3. Verify budget pricing doesn't trigger false fraud alert
4. Verify simple description is acceptable
5. Check all modules show low scores

---

## 🔴 PRICE FRAUD (Expected: High Fraud Probability > 0.5)

### Test Case P1: Severely Underpriced Property

**Category**: Price Fraud (Underpriced)  
**Expected Fraud Probability**: 0.60 - 0.85  
**Expected Fraud Types**: ["Price Fraud"]  

**Input Data**:
```json
{
  "title": "3BHK Apartment in Andheri West",
  "description": "Spacious 3BHK apartment with modern amenities, parking, and good connectivity. Well-maintained building with lift and security.",
  "price": 1500000,
  "area_sqft": 1400,
  "city": "Mumbai",
  "locality": "Andheri West",
  "latitude": 19.1334,
  "longitude": 72.8291
}
```

**Why It's Fraudulent**:
- Market price for 3BHK in Andheri West: ₹8-12 million
- Listed price: ₹1.5 million (80-90% below market)
- Suspiciously low for the area and size

**Expected Output**:
- Fraud Probability: ~0.70 - 0.85
- Fraud Types: ["Price Fraud"]
- Price Score: > 0.80
- Text Score: < 0.3
- Location Score: < 0.3
- Explanations: "Price is significantly below market average for Andheri West", "Price deviation: -75% to -85%"

**Test Steps**:
1. Enter all fields with suspiciously low price
2. Submit for analysis
3. Verify HIGH fraud probability (red indicator)
4. Verify "Price Fraud" is flagged
5. Check price module score is very high (> 0.80)
6. Read explanation about price deviation

---

### Test Case P2: Overpriced Property

**Category**: Price Fraud (Overpriced)  
**Expected Fraud Probability**: 0.55 - 0.75  
**Expected Fraud Types**: ["Price Fraud"]  

**Input Data**:
```json
{
  "title": "2BHK Flat in Malad",
  "description": "Standard 2BHK flat with basic amenities. Suitable for families. Close to local market and transport.",
  "price": 15000000,
  "area_sqft": 900,
  "city": "Mumbai",
  "locality": "Malad East",
  "latitude": 19.1868,
  "longitude": 72.8493
}
```

**Why It's Fraudulent**:
- Market price for 2BHK in Malad East: ₹4-6 million
- Listed price: ₹15 million (150-250% above market)
- Unrealistic pricing for standard flat

**Expected Output**:
- Fraud Probability: ~0.60 - 0.75
- Fraud Types: ["Price Fraud"]
- Price Score: > 0.75
- Text Score: < 0.3
- Location Score: < 0.3
- Explanations: "Price is significantly above market average", "Overpriced by 150-200%"

**Test Steps**:
1. Enter all fields with inflated price
2. Submit for analysis
3. Verify HIGH fraud probability
4. Verify "Price Fraud" is detected
5. Check price module shows high score
6. Verify explanation mentions overpricing

---

## 🟡 TEXT FRAUD (Expected: Medium-High Fraud Probability 0.4 - 0.7)

### Test Case T1: Urgency and Scam Keywords

**Category**: Text Fraud (Urgency + Scam)  
**Expected Fraud Probability**: 0.50 - 0.70  
**Expected Fraud Types**: ["Text Fraud"]  

**Input Data**:
```json
{
  "title": "URGENT SALE! Don't Miss This Amazing Deal!",
  "description": "HURRY! LIMITED TIME OFFER! This is a GUARANTEED investment opportunity. 100% SAFE and RISK-FREE property. Act now before it's gone! Cash only, advance payment required. Wire transfer accepted. This is a once in a lifetime chance!",
  "price": 5000000,
  "area_sqft": 1200,
  "city": "Mumbai",
  "locality": "Andheri West",
  "latitude": 19.1334,
  "longitude": 72.8291
}
```

**Why It's Fraudulent**:
- Multiple urgency keywords: "URGENT", "HURRY", "LIMITED TIME", "ACT NOW"
- Scam indicators: "GUARANTEED", "100% SAFE", "RISK-FREE"
- Suspicious payment terms: "Cash only", "advance payment", "wire transfer"
- Excessive capitalization and exclamation marks

**Expected Output**:
- Fraud Probability: ~0.55 - 0.70
- Fraud Types: ["Text Fraud"]
- Price Score: < 0.4
- Text Score: > 0.70
- Location Score: < 0.3
- Explanations: "Description contains urgency keywords", "Suspicious payment terms detected", "Excessive use of promotional language"

**Test Steps**:
1. Enter all fields with suspicious text
2. Submit for analysis
3. Verify MEDIUM-HIGH fraud probability (yellow/orange indicator)
4. Verify "Text Fraud" is flagged
5. Check text module score is high (> 0.70)
6. Read explanations about suspicious keywords

---

### Test Case T2: Exaggeration and Manipulation

**Category**: Text Fraud (Exaggeration)  
**Expected Fraud Probability**: 0.45 - 0.65  
**Expected Fraud Types**: ["Text Fraud"]  

**Input Data**:
```json
{
  "title": "ULTIMATE LUXURY PREMIUM EXCLUSIVE WORLD-CLASS Property",
  "description": "This is the BEST, most AMAZING, INCREDIBLE, UNBELIEVABLE property you will ever find! PERFECT in every way! The most EXCLUSIVE and PREMIUM apartment in the ENTIRE city! This is GUARANTEED to be the ULTIMATE investment!",
  "price": 8000000,
  "area_sqft": 1500,
  "city": "Mumbai",
  "locality": "Bandra West",
  "latitude": 19.0596,
  "longitude": 72.8295
}
```

**Why It's Fraudulent**:
- Excessive exaggeration keywords: "ULTIMATE", "BEST", "AMAZING", "INCREDIBLE", "UNBELIEVABLE", "PERFECT"
- Unrealistic claims: "ENTIRE city", "GUARANTEED"
- Manipulative language designed to pressure buyers

**Expected Output**:
- Fraud Probability: ~0.50 - 0.65
- Fraud Types: ["Text Fraud"]
- Price Score: < 0.4
- Text Score: > 0.65
- Location Score: < 0.3
- Explanations: "Excessive use of superlatives", "Manipulative language detected", "Unrealistic claims in description"

**Test Steps**:
1. Enter all fields with exaggerated text
2. Submit for analysis
3. Verify MEDIUM-HIGH fraud probability
4. Verify "Text Fraud" is detected
5. Check text module flags excessive exaggeration
6. Verify explanation mentions superlatives

---

## 🟠 LOCATION FRAUD (Expected: Medium Fraud Probability 0.4 - 0.6)

### Test Case L1: Coordinate Mismatch

**Category**: Location Fraud  
**Expected Fraud Probability**: 0.45 - 0.65  
**Expected Fraud Types**: ["Location Fraud"]  

**Input Data**:
```json
{
  "title": "Beautiful 2BHK Apartment in Andheri West",
  "description": "Well-maintained apartment in prime Andheri West location. Close to metro station, schools, and shopping centers. Excellent connectivity.",
  "price": 6500000,
  "area_sqft": 1100,
  "city": "Mumbai",
  "locality": "Andheri West",
  "latitude": 18.5204,
  "longitude": 73.8567
}
```

**Why It's Fraudulent**:
- Claimed location: Andheri West, Mumbai
- Actual coordinates: 18.5204°N, 73.8567°E (Pune area, ~150km from Mumbai)
- Andheri West coordinates should be: ~19.13°N, 72.83°E
- Massive coordinate mismatch (>100km)

**Expected Output**:
- Fraud Probability: ~0.50 - 0.65
- Fraud Types: ["Location Fraud"]
- Price Score: < 0.3
- Text Score: < 0.3
- Location Score: > 0.70
- Explanations: "Coordinates do not match stated locality", "Distance mismatch: ~150km", "Possible location fraud"

**Test Steps**:
1. Enter all fields with mismatched coordinates
2. Submit for analysis
3. Verify MEDIUM fraud probability
4. Verify "Location Fraud" is flagged
5. Check location module score is high
6. Read explanation about coordinate mismatch
7. Verify distance calculation in explanation

---

## 🔴 MULTI-FRAUD (Expected: Very High Fraud Probability > 0.7)

### Test Case M1: Combined Price + Text + Location Fraud

**Category**: Multi-Fraud (All Types)  
**Expected Fraud Probability**: 0.75 - 0.95  
**Expected Fraud Types**: ["Price Fraud", "Text Fraud", "Location Fraud"]  

**Input Data**:
```json
{
  "title": "URGENT! AMAZING 3BHK - ONCE IN LIFETIME DEAL!",
  "description": "HURRY! LIMITED TIME! This GUARANTEED 100% SAFE investment is UNBELIEVABLE! The BEST property EVER! Act now, cash only, advance payment required. Don't miss this INCREDIBLE opportunity!",
  "price": 1200000,
  "area_sqft": 1600,
  "city": "Mumbai",
  "locality": "Bandra West",
  "latitude": 18.9220,
  "longitude": 72.8347
}
```

**Why It's Fraudulent**:
1. **Price Fraud**: ₹1.2M for 1600 sqft in Bandra West (should be ₹15-20M)
2. **Text Fraud**: Urgency keywords, scam indicators, suspicious payment terms
3. **Location Fraud**: Coordinates point to South Mumbai, not Bandra West

**Expected Output**:
- Fraud Probability: ~0.80 - 0.95
- Fraud Types: ["Price Fraud", "Text Fraud", "Location Fraud"]
- Price Score: > 0.85
- Text Score: > 0.75
- Location Score: > 0.65
- Explanations: Multiple warnings about price, text, and location anomalies

**Test Steps**:
1. Enter all fields with multiple fraud indicators
2. Submit for analysis
3. Verify VERY HIGH fraud probability (dark red indicator)
4. Verify ALL fraud types are flagged
5. Check all module scores are high
6. Read comprehensive fraud warnings
7. Verify fusion engine combines all signals

---

## 📊 Test Case Summary Table

| ID | Category | Title | Price (₹) | Area (sqft) | Expected Fraud | Expected Types |
|----|----------|-------|-----------|-------------|----------------|----------------|
| N1 | Normal | Spacious 2BHK Apartment | 4,500,000 | 1,100 | 0.10-0.20 | None |
| N2 | Normal | Premium 3BHK Penthouse | 12,500,000 | 2,200 | 0.15-0.25 | None |
| N3 | Normal | Affordable 1BHK Flat | 2,800,000 | 550 | 0.10-0.20 | None |
| P1 | Price Fraud | 3BHK Apartment (Underpriced) | 1,500,000 | 1,400 | 0.70-0.85 | Price Fraud |
| P2 | Price Fraud | 2BHK Flat (Overpriced) | 15,000,000 | 900 | 0.60-0.75 | Price Fraud |
| T1 | Text Fraud | URGENT SALE! | 5,000,000 | 1,200 | 0.55-0.70 | Text Fraud |
| T2 | Text Fraud | ULTIMATE LUXURY | 8,000,000 | 1,500 | 0.50-0.65 | Text Fraud |
| L1 | Location Fraud | Andheri West (Wrong Coords) | 6,500,000 | 1,100 | 0.50-0.65 | Location Fraud |
| M1 | Multi-Fraud | URGENT 3BHK DEAL | 1,200,000 | 1,600 | 0.80-0.95 | All Types |

---

## 🧪 Testing Procedure

### Pre-Test Setup

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   Verify: http://localhost:8000/health shows "healthy"

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
   Verify: http://localhost:5173 loads successfully

3. **Check Dataset**:
   - Ensure `backend/app/data/real_estate.csv` exists
   - Backend should log: "✅ Dataset loaded: XXXX properties"

4. **Clear Browser Console**:
   - Open DevTools (F12)
   - Clear console
   - Check for any errors

### Test Execution Steps

For each test case:

1. **Navigate to Form**:
   - Go to http://localhost:5173
   - Ensure form is visible

2. **Enter Test Data**:
   - Copy input data from test case
   - Fill all 8 fields:
     - Title
     - Description
     - Price
     - Area (sqft)
     - City
     - Locality
     - Latitude
     - Longitude

3. **Submit Analysis**:
   - Click "Initialize Fraud Detection Sequence"
   - Observe loading spinner
   - Wait for results (2-5 seconds)

4. **Verify Results**:
   - Check fraud probability matches expected range
   - Verify fraud types match expected list
   - Check module scores (Price, Text, Location, Image)
   - Read explanations for accuracy

5. **Document Results**:
   - Screenshot the results dashboard
   - Note actual fraud probability
   - Note actual fraud types
   - Note any discrepancies

6. **Return to Form**:
   - Click "Return to Dashboard"
   - Verify form is ready for next test

### Post-Test Verification

1. **Check History**:
   - Click "Fraud Database" tab
   - Verify all test cases are saved
   - Check timestamps are correct

2. **Check Console**:
   - Verify no errors in browser console
   - Verify no errors in backend logs

3. **Performance Check**:
   - Verify analysis completes in < 5 seconds
   - Verify UI is responsive
   - Verify no memory leaks

---

## 📋 Test Results Template

### Test Case: [ID] - [Category]

**Date**: ___________  
**Tester**: ___________  
**Environment**: Development / Production  

**Input Data**:
- Title: ___________
- Price: ___________
- Area: ___________
- Locality: ___________

**Expected Results**:
- Fraud Probability: ___________
- Fraud Types: ___________

**Actual Results**:
- Fraud Probability: ___________
- Fraud Types: ___________
- Price Score: ___________
- Text Score: ___________
- Location Score: ___________

**Status**: ✅ PASS / ❌ FAIL  

**Notes**:
___________________________________________
___________________________________________

**Screenshots**: Attached / Not Attached  

---

## 🎯 Demo Sequence (Recommended Order)

### For Live Demo (10 minutes)

**1. Introduction (1 min)**
- Show homepage
- Explain system purpose
- Point out clean UI

**2. Normal Listing (1.5 min)**
- Use Test Case N1 (Spacious 2BHK)
- Show LOW fraud probability
- Explain green indicator means safe

**3. Price Fraud (2 min)**
- Use Test Case P1 (Underpriced 3BHK)
- Show HIGH fraud probability
- Explain price deviation detection
- Point out red indicator

**4. Text Fraud (2 min)**
- Use Test Case T1 (URGENT SALE)
- Show suspicious keywords detection
- Explain text analysis module
- Point out specific warnings

**5. Location Fraud (1.5 min)**
- Use Test Case L1 (Coordinate Mismatch)
- Show location verification
- Explain distance calculation

**6. Multi-Fraud (2 min)**
- Use Test Case M1 (Combined Fraud)
- Show all modules detecting fraud
- Explain fusion engine
- Point out very high probability

**7. History & Wrap-up (1 min)**
- Show "Fraud Database" tab
- Display all analyzed listings
- Summarize system capabilities

---

## 🔍 Edge Cases to Test (Optional)

### Edge Case 1: Empty Description
**Input**: All fields valid except description = ""  
**Expected**: Validation error before submission  

### Edge Case 2: Zero Price
**Input**: price = 0  
**Expected**: Validation error: "Price cannot be zero"  

### Edge Case 3: Invalid Coordinates
**Input**: latitude = 100 (out of range)  
**Expected**: Validation error: "Latitude must be between -90 and 90"  

### Edge Case 4: Very Long Title
**Input**: title = 500+ characters  
**Expected**: Either truncation or validation error  

### Edge Case 5: Special Characters
**Input**: description with emojis, special symbols  
**Expected**: System handles gracefully, no crashes  

---

## 📊 Expected System Behavior

### Fraud Probability Ranges

| Range | Color | Interpretation | Action |
|-------|-------|----------------|--------|
| 0.00 - 0.30 | 🟢 Green | Low Risk | Safe to proceed |
| 0.31 - 0.50 | 🟡 Yellow | Medium Risk | Caution advised |
| 0.51 - 0.70 | 🟠 Orange | High Risk | Further investigation |
| 0.71 - 1.00 | 🔴 Red | Very High Risk | Likely fraud |

### Module Score Interpretation

| Module | Weight | High Score Threshold |
|--------|--------|---------------------|
| Price | 30% | > 0.60 |
| Image | 25% | > 0.60 |
| Text | 25% | > 0.60 |
| Location | 20% | > 0.60 |

### Response Time Benchmarks

| Operation | Expected Time | Max Acceptable |
|-----------|---------------|----------------|
| Form Load | < 1 second | 2 seconds |
| Analysis | 2-5 seconds | 10 seconds |
| History Load | < 2 seconds | 5 seconds |
| Navigation | < 0.5 seconds | 1 second |

---

## ✅ Test Completion Checklist

### Before Demo
- [ ] Backend running and healthy
- [ ] Frontend running and accessible
- [ ] Dataset loaded successfully
- [ ] No console errors
- [ ] All test cases prepared
- [ ] Screenshots folder ready

### During Testing
- [ ] Test Case N1 executed
- [ ] Test Case N2 executed
- [ ] Test Case N3 executed
- [ ] Test Case P1 executed
- [ ] Test Case P2 executed
- [ ] Test Case T1 executed
- [ ] Test Case T2 executed
- [ ] Test Case L1 executed
- [ ] Test Case M1 executed

### After Testing
- [ ] All results documented
- [ ] Screenshots captured
- [ ] History verified
- [ ] Performance acceptable
- [ ] No bugs found
- [ ] System stable

---

## 🐛 Known Issues / Notes

### Issue 1: Image Module Placeholder
**Status**: Expected  
**Impact**: Image fraud score always 0.0  
**Note**: Image module not implemented, this is documented limitation  

### Issue 2: Text Module Sensitivity
**Status**: Normal  
**Impact**: May not flag subtle text fraud  
**Note**: Uses keyword matching, not semantic analysis  

### Issue 3: Price Variance by Locality
**Status**: Expected  
**Impact**: Some localities have high price variance  
**Note**: System uses statistical thresholds, may miss fraud in high-variance areas  

---

## 📝 Test Report Template

### Executive Summary

**Test Date**: ___________  
**System Version**: 2.1.0  
**Total Test Cases**: 9  
**Passed**: _____ / 9  
**Failed**: _____ / 9  
**Pass Rate**: _____% 

### Detailed Results

| Test ID | Category | Status | Fraud Probability | Notes |
|---------|----------|--------|-------------------|-------|
| N1 | Normal | ✅/❌ | _____ | _____ |
| N2 | Normal | ✅/❌ | _____ | _____ |
| N3 | Normal | ✅/❌ | _____ | _____ |
| P1 | Price Fraud | ✅/❌ | _____ | _____ |
| P2 | Price Fraud | ✅/❌ | _____ | _____ |
| T1 | Text Fraud | ✅/❌ | _____ | _____ |
| T2 | Text Fraud | ✅/❌ | _____ | _____ |
| L1 | Location Fraud | ✅/❌ | _____ | _____ |
| M1 | Multi-Fraud | ✅/❌ | _____ | _____ |

### Issues Found

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

### Recommendations

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

### Conclusion

___________________________________________
___________________________________________
___________________________________________

**Tester Signature**: ___________  
**Date**: ___________

---

## 🎓 For Academic Evaluation

### What to Highlight

1. **Comprehensive Testing**: 9 test cases covering all fraud types
2. **Realistic Scenarios**: Based on actual real estate fraud patterns
3. **Systematic Approach**: Structured test cases with expected outputs
4. **Documentation**: Detailed test plan and results template

### Demo Tips

1. **Start with Normal**: Show system doesn't flag legitimate listings
2. **Show Fraud Detection**: Demonstrate each fraud type clearly
3. **Explain Fusion**: Show how multiple modules combine
4. **Handle Questions**: Be ready to explain any test case

### Viva Questions

**Q: How did you test the system?**  
**A**: "We designed 9 comprehensive test cases covering normal listings and all fraud types. Each test case has defined inputs and expected outputs for systematic verification."

**Q: What if the system fails a test?**  
**A**: "We document the failure, analyze the root cause, and either fix the bug or adjust thresholds. The test cases help identify edge cases and improve the system."

**Q: How do you ensure test coverage?**  
**A**: "We test each fraud module independently (price, text, location) and in combination (multi-fraud). We also test normal listings to verify no false positives."

---

## 🏆 Success Criteria

### System Passes If:

✅ **Normal Listings**: All 3 show fraud probability < 0.30  
✅ **Price Fraud**: Both show fraud probability > 0.50 with "Price Fraud" flagged  
✅ **Text Fraud**: Both show fraud probability > 0.40 with "Text Fraud" flagged  
✅ **Location Fraud**: Shows fraud probability > 0.40 with "Location Fraud" flagged  
✅ **Multi-Fraud**: Shows fraud probability > 0.70 with multiple types flagged  
✅ **Performance**: All analyses complete in < 10 seconds  
✅ **Stability**: No crashes or errors during testing  
✅ **UI/UX**: Clear display of results, no console errors  

---

**Test Plan Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: ✅ Ready for Execution  
**Prepared By**: QA Engineer  

---

*This test plan is ready for live demo and academic evaluation. All test cases are designed to demonstrate the system's fraud detection capabilities comprehensively.*
