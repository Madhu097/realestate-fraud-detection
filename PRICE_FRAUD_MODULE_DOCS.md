# 🎓 EXAMINER-PROOF PRICE FRAUD DETECTION

## Module Status: FROZEN ✅
**Finalized on Day 4 - Do not modify unless required for fusion**

---

## 📊 Statistical Methods Implemented

### Method 1: Z-Score Analysis
**Purpose:** Detect deviations from mean using standard deviations

**Formula:**
```
z-score = |listing_price - mean_price| / std_deviation
fraud_score_z = min(z_score / 3.0, 1.0)
```

**Interpretation:**
- z-score > 3: 99.7% anomaly (3-sigma rule)
- z-score > 2: 95% anomaly
- z-score > 1: 68% anomaly

**Limitation:** Sensitive to outliers and skewed distributions

---

### Method 2: IQR (Interquartile Range) Analysis
**Purpose:** Robust outlier detection using quartiles

**Formula:**
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

**Detection Logic:**
- If price < Lower Bound → Suspicious (too low)
- If price > Upper Bound → Suspicious (too high)
- Otherwise → Normal

**Advantage:** Not affected by extreme outliers (robust to skewed data)

---

## 🔬 Combined Approach (Examiner-Approved)

### Why Combine?
1. **Z-Score alone:** Breaks with skewed data, sensitive to outliers
2. **IQR alone:** May miss subtle anomalies
3. **Combined:** Maximum sensitivity + robustness

### Combination Logic:
```python
final_fraud_score = max(z_score_normalized, iqr_score)
```

**Justification for Examiners:**
- Takes the **maximum** of both methods
- Ensures we don't miss fraud detected by either method
- Provides statistical robustness
- Industry-standard approach for anomaly detection

---

## 🛡️ Edge Cases Handled

### 1. Very Small Locality Samples (< 5 properties)
**Response:**
```
fraud_score = 0.0
explanation = "Insufficient comparable listings in '{locality}' for reliable price analysis."
```

**Why:** Cannot perform reliable statistical analysis with < 5 samples

---

### 2. Zero Variance (All prices identical)
**Scenario A:** Listing price matches standard price
```
fraud_score = 0.0
explanation = "The listed price matches the standard price for '{locality}'."
```

**Scenario B:** Listing price differs
```
fraud_score = 0.8
explanation = "All properties in '{locality}' are priced at ₹X, but this listing is Y% different."
```

**Why:** Any deviation from uniform pricing is highly suspicious

---

### 3. Missing Locality
**Response:**
```
fraud_score = 0.0
explanation = "Insufficient comparable listings..."
```

**Why:** Cannot compare without reference data

---

### 4. Extreme Prices
**Handled by:** IQR bounds automatically flag extreme outliers
**Result:** High fraud score + detailed explanation with bounds

---

## 📝 Examiner-Approved Explanations

### ❌ BAD (Technical Jargon):
```
"Price deviates from locality average"
"Z-score exceeds threshold"
```

### ✅ GOOD (Clear, Contextual):
```
"The listed price of ₹1,000,000 is 80.8% below the average price of similar 
properties in 'Kharghar', which is statistically unusual. Average: ₹5,200,000, 
Median: ₹5,000,000. This price falls below the normal range 
(₹3,500,000 - ₹7,000,000) and may indicate fraud or data entry error."
```

### Key Elements:
1. ✅ Actual price mentioned
2. ✅ Percentage deviation
3. ✅ Locality context
4. ✅ Statistical reference (mean, median)
5. ✅ IQR bounds (when applicable)
6. ✅ Clear conclusion
7. ❌ No technical jargon

---

## 🧪 Test Cases (All Must Pass)

### Test 1: Normal Price
**Input:** ₹5,000,000 in Kharghar  
**Expected:** fraud_score < 0.3  
**Explanation:** "Price is within normal range..."

---

### Test 2: Very Low Price
**Input:** ₹1,000,000 in Kharghar  
**Expected:** fraud_score > 0.6  
**Fraud Type:** "price_manipulation"  
**Explanation:** "80.8% below average... falls below normal range..."

---

### Test 3: Very High Price
**Input:** ₹15,000,000 in Kharghar  
**Expected:** fraud_score 0.3 - 0.9  
**Explanation:** "X% above average... exceeds normal range..."

---

### Test 4: Unknown Locality
**Input:** Any price in "NonExistentPlace"  
**Expected:** fraud_score = 0.0  
**Explanation:** "Insufficient comparable listings..."

---

### Test 5: Extreme Price (IQR Test)
**Input:** ₹500,000 in Kharghar  
**Expected:** fraud_score > 0.8  
**Explanation:** Must mention "normal range" with bounds

---

## 🎯 Viva Questions & Answers

### Q1: Why use both Z-Score and IQR?
**A:** Z-score is sensitive to outliers and breaks with skewed distributions. IQR is robust to outliers but may miss subtle anomalies. Combining both (taking maximum) gives us the best of both worlds - sensitivity and robustness.

---

### Q2: Why take maximum instead of average?
**A:** We want to detect fraud, not average it out. If either method flags high risk, we should investigate. Taking maximum ensures we don't miss potential fraud detected by either method.

---

### Q3: What if locality has < 5 samples?
**A:** We return fraud_score = 0.0 with explanation about insufficient data. This is statistically honest - we cannot make reliable inferences with very small samples.

---

### Q4: How do you handle skewed price distributions?
**A:** That's exactly why we use IQR in addition to Z-score. IQR uses quartiles which are robust to skewness, while Z-score assumes normal distribution. The combination handles both scenarios.

---

### Q5: What's the significance of 1.5 × IQR?
**A:** This is the standard statistical threshold for outlier detection (Tukey's method). Values beyond Q1 - 1.5×IQR or Q3 + 1.5×IQR are considered outliers in boxplot analysis.

---

### Q6: Why normalize z-score by dividing by 3?
**A:** Based on the 3-sigma rule (99.7% of data falls within 3 standard deviations). A z-score of 3 or more indicates an extreme anomaly, which we map to fraud_score = 1.0.

---

## 📚 Code Structure

```
price_fraud.py
├── Header Comment: "Finalized on Day 4"
├── Module Docstring: Methods explanation
├── detect_price_fraud()
│   ├── Filter by locality
│   ├── Edge Case 1: Small samples
│   ├── Edge Case 2: Zero variance
│   ├── Method 1: Z-Score
│   ├── Method 2: IQR
│   ├── Combination: max(z, iqr)
│   └── Generate explanation
└── Return (fraud_score, explanation)
```

---

## ✅ Checklist for Examiners

- [x] Uses multiple statistical methods (Z-Score + IQR)
- [x] Handles edge cases properly
- [x] Provides clear, non-technical explanations
- [x] Includes percentage deviations
- [x] Mentions locality context
- [x] Shows statistical references (mean, median, bounds)
- [x] Frozen and documented
- [x] All test cases pass
- [x] Viva questions prepared

---

## 🚀 Integration Status

**File:** `backend/app/services/price_fraud.py`  
**Status:** ✅ FROZEN  
**Last Modified:** Day 4  
**Lines of Code:** ~160  
**Test Coverage:** 5 test cases  
**Documentation:** Complete  

---

**This module is production-ready and examiner-proof.** 🎓
