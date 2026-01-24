# Live Demo - Final Preparation Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Start Backend
```bash
cd backend
uvicorn app.main:app --reload
```
**Verify**: Visit http://localhost:8000/health → Should show "healthy"

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```
**Verify**: Visit http://localhost:5173 → Form should load

### Step 3: Open Demo Files
- Keep `QUICK_DEMO_INPUTS.md` open for copy-paste
- Keep browser console open (F12) to verify no errors

---

## 🎯 5-Test Demo Sequence (10 Minutes)

### Test 1: Normal Listing ✅ (2 min)
**Purpose**: Show system doesn't flag legitimate listings

**Copy-Paste This**:
```
Title: Spacious 2BHK Apartment in Prime Location
Description: Well-maintained 2BHK apartment with 2 bathrooms, modular kitchen, and covered parking. Located in a peaceful residential area with good connectivity to schools and hospitals.
Price: 4500000
Area: 1100
City: Mumbai
Locality: Andheri West
Latitude: 19.1334
Longitude: 72.8291
```

**Expected**: 
- Fraud Probability: 0.10-0.20 (GREEN)
- Fraud Types: None
- All module scores LOW

**What to Say**: 
"This is a legitimate 2BHK listing in Andheri West. The system correctly identifies it as low risk with a fraud probability around 15%."

---

### Test 2: Price Fraud 🔴 (2 min)
**Purpose**: Demonstrate price anomaly detection

**Copy-Paste This**:
```
Title: 3BHK Apartment in Andheri West
Description: Spacious 3BHK apartment with modern amenities, parking, and good connectivity. Well-maintained building with lift and security.
Price: 1500000
Area: 1400
City: Mumbai
Locality: Andheri West
Latitude: 19.1334
Longitude: 72.8291
```

**Expected**:
- Fraud Probability: 0.70-0.85 (RED)
- Fraud Types: ["Price Fraud"]
- Price Score: > 0.80

**What to Say**:
"This 3BHK in the same area is priced at only ₹15 lakhs, which is 80-90% below market value of ₹80-120 lakhs. The system correctly flags this as high-risk price fraud."

---

### Test 3: Text Fraud 🟡 (2 min)
**Purpose**: Show suspicious keyword detection

**Copy-Paste This**:
```
Title: URGENT SALE! Don't Miss This Amazing Deal!
Description: HURRY! LIMITED TIME OFFER! This is a GUARANTEED investment opportunity. 100% SAFE and RISK-FREE property. Act now before it's gone! Cash only, advance payment required. Wire transfer accepted. This is a once in a lifetime chance!
Price: 5000000
Area: 1200
City: Mumbai
Locality: Andheri West
Latitude: 19.1334
Longitude: 72.8291
```

**Expected**:
- Fraud Probability: 0.55-0.70 (ORANGE)
- Fraud Types: ["Text Fraud"]
- Text Score: > 0.70

**What to Say**:
"Notice the urgency keywords like URGENT, HURRY, LIMITED TIME, and scam indicators like GUARANTEED, 100% SAFE, cash only. The system detects these suspicious patterns."

---

### Test 4: Location Fraud 🟠 (2 min)
**Purpose**: Demonstrate coordinate verification

**Copy-Paste This**:
```
Title: Beautiful 2BHK Apartment in Andheri West
Description: Well-maintained apartment in prime Andheri West location. Close to metro station, schools, and shopping centers. Excellent connectivity.
Price: 6500000
Area: 1100
City: Mumbai
Locality: Andheri West
Latitude: 18.5204
Longitude: 73.8567
```

**Expected**:
- Fraud Probability: 0.50-0.65 (ORANGE)
- Fraud Types: ["Location Fraud"]
- Location Score: > 0.70

**What to Say**:
"The listing claims to be in Andheri West, Mumbai, but the coordinates actually point to Pune, about 150km away. The system detects this geographic mismatch."

---

### Test 5: Multi-Fraud 🔴 (2 min)
**Purpose**: Show fusion engine combining multiple signals

**Copy-Paste This**:
```
Title: URGENT! AMAZING 3BHK - ONCE IN LIFETIME DEAL!
Description: HURRY! LIMITED TIME! This GUARANTEED 100% SAFE investment is UNBELIEVABLE! The BEST property EVER! Act now, cash only, advance payment required. Don't miss this INCREDIBLE opportunity!
Price: 1200000
Area: 1600
City: Mumbai
Locality: Bandra West
Latitude: 18.9220
Longitude: 72.8347
```

**Expected**:
- Fraud Probability: 0.80-0.95 (DARK RED)
- Fraud Types: ["Price Fraud", "Text Fraud", "Location Fraud"]
- All module scores HIGH

**What to Say**:
"This listing combines all fraud types: severely underpriced, suspicious keywords, and wrong coordinates. The fusion engine correctly identifies this as very high risk with 85-90% fraud probability."

---

## 📊 Quick Reference Table

| # | Type | Price | Expected Fraud | Key Point |
|---|------|-------|----------------|-----------|
| 1 | Normal | ₹45L | 0.10-0.20 🟢 | Legitimate listing |
| 2 | Price | ₹15L | 0.70-0.85 🔴 | 80% underpriced |
| 3 | Text | ₹50L | 0.55-0.70 🟡 | Urgency + scam keywords |
| 4 | Location | ₹65L | 0.50-0.65 🟠 | 150km coordinate mismatch |
| 5 | Multi | ₹12L | 0.80-0.95 🔴 | All fraud types combined |

---

## ✅ Pre-Demo Checklist

**5 Minutes Before Demo**:
- [ ] Backend running and healthy
- [ ] Frontend loaded successfully
- [ ] Dataset loaded (check backend logs)
- [ ] Browser console clear (no errors)
- [ ] QUICK_DEMO_INPUTS.md open
- [ ] This guide open

**During Demo**:
- [ ] Explain each test case before submitting
- [ ] Point out fraud probability color coding
- [ ] Show module scores breakdown
- [ ] Read fraud explanations
- [ ] Demonstrate "Return to Dashboard" flow

**After Demo**:
- [ ] Show "Fraud Database" tab with history
- [ ] Verify all 5 tests are saved
- [ ] Answer questions confidently

---

## 🎬 Demo Script Template

**[Introduction - 30 seconds]**
"This is Truth in Listings, a hybrid AI fraud detection system for real estate. It analyzes price distribution, text patterns, and geospatial data to identify fraudulent listings. Let me demonstrate with 5 test cases."

**[Test 1 - Normal - 2 min]**
"First, a legitimate 2BHK apartment..."
*Submit, show results*
"As you can see, fraud probability is low at 15%, shown in green. No fraud types are flagged."

**[Test 2 - Price - 2 min]**
"Now, the same area but suspiciously underpriced..."
*Submit, show results*
"The system detects this is 80% below market value and flags it as high-risk price fraud."

**[Test 3 - Text - 2 min]**
"This listing has urgency keywords and scam indicators..."
*Submit, show results*
"Notice how the text module identifies suspicious patterns like URGENT, GUARANTEED, cash only."

**[Test 4 - Location - 2 min]**
"Here the coordinates don't match the claimed location..."
*Submit, show results*
"The system calculates the property is 150km from where it claims to be."

**[Test 5 - Multi - 2 min]**
"Finally, a listing with all fraud types combined..."
*Submit, show results*
"The fusion engine combines all signals, showing 90% fraud probability with all types flagged."

**[Conclusion - 30 seconds]**
"The system successfully detects price anomalies, suspicious text, location fraud, and combinations. All results are saved in the fraud database for audit purposes."

---

## 🎓 Viva Q&A - Quick Answers

**Q: How does the system detect fraud?**
**A**: "It uses a hybrid approach with 4 modules: price analysis (statistical deviation), text analysis (keyword matching), location verification (coordinate validation), and a fusion engine that combines all signals with weighted scoring."

**Q: What's the accuracy?**
**A**: "In our evaluation on 400 synthetic listings, we achieved 100% precision (no false positives) with 1.5% recall. The system is conservative to avoid falsely accusing legitimate sellers."

**Q: Can it detect all fraud?**
**A**: "No system is perfect. We acknowledge limitations: the image module is a placeholder, text analysis uses keywords not semantics, and we've only tested on synthetic fraud. But it successfully demonstrates the multi-module fusion concept."

**Q: How do you handle false positives?**
**A**: "The system is designed to be conservative with a 0.5 fusion threshold. We prioritize precision over recall to minimize false accusations."

**Q: What's the fusion engine?**
**A**: "It's a weighted linear combination: Price (30%), Image (25%), Text (25%), Location (20%). Scores above 0.6 in any module contribute to fraud type identification."

**Q: How fast is it?**
**A**: "Analysis completes in 2-5 seconds. The backend uses FastAPI for performance, and we cache the dataset in memory."

---

## 🐛 Troubleshooting

### Issue: "Network Error"
**Fix**: Backend not running
```bash
cd backend
uvicorn app.main:app --reload
```

### Issue: "Dataset not loaded"
**Fix**: Missing CSV file
- Check `backend/app/data/real_estate.csv` exists
- Restart backend

### Issue: CORS Error
**Fix**: Port mismatch
- Backend should be on 8000
- Frontend should be on 5173
- Check API_BASE_URL in App.jsx

### Issue: Validation Error
**Fix**: Check input format
- Price must be > 0
- Area must be > 0
- Latitude: -90 to 90
- Longitude: -180 to 180

---

## 📸 Screenshot Opportunities

1. **Form View** - Clean, professional input form
2. **Loading State** - Spinner during analysis
3. **Normal Result** - Green indicator, low fraud
4. **Price Fraud** - Red indicator, high score
5. **Text Fraud** - Orange indicator, keywords
6. **Multi-Fraud** - Dark red, all types flagged
7. **History View** - All tests saved
8. **Module Scores** - Breakdown chart

---

## ⏱️ Time Management

**Total Demo**: 10-12 minutes

- Introduction: 0:30
- Test 1 (Normal): 2:00
- Test 2 (Price): 2:00
- Test 3 (Text): 2:00
- Test 4 (Location): 2:00
- Test 5 (Multi): 2:00
- History + Conclusion: 1:00
- Q&A Buffer: 2:00

**If Short on Time**: Skip Test 4 (Location), do 4 tests in 8 minutes

---

## 🏆 Success Indicators

Demo is successful if:

✅ All 5 tests complete without errors  
✅ Fraud probabilities match expected ranges  
✅ Fraud types are correctly identified  
✅ Module scores are reasonable  
✅ UI displays results clearly  
✅ No console errors  
✅ History saves all tests  
✅ Questions answered confidently  

---

## 📝 Post-Demo Notes Template

**Demo Date**: ___________  
**Audience**: ___________  
**Duration**: ___________  

**Tests Executed**:
- [ ] Normal Listing
- [ ] Price Fraud
- [ ] Text Fraud
- [ ] Location Fraud
- [ ] Multi-Fraud

**Results**:
- All tests passed: Yes / No
- Any errors: Yes / No
- Questions asked: ___________

**Feedback**:
___________________________________________
___________________________________________

**Improvements Needed**:
___________________________________________
___________________________________________

---

## 🎯 Key Takeaways for Evaluators

1. **Multi-Module Approach**: Price, Text, Location, Image (placeholder)
2. **Fusion Engine**: Weighted combination with explainable results
3. **Conservative Design**: High precision, low false positives
4. **Academic Honesty**: Acknowledges synthetic data and limitations
5. **Production-Ready Code**: Clean architecture, error handling, documentation

---

## ✅ Final Pre-Demo Checklist

**30 Minutes Before**:
- [ ] Test all 5 cases once
- [ ] Verify results match expectations
- [ ] Clear browser history/cache
- [ ] Close unnecessary applications
- [ ] Charge laptop / check power

**10 Minutes Before**:
- [ ] Start backend
- [ ] Start frontend
- [ ] Verify both running
- [ ] Open demo files
- [ ] Clear console

**Ready to Demo**:
- [ ] Confident with test cases
- [ ] Know expected outputs
- [ ] Prepared for questions
- [ ] Relaxed and ready

---

**You're ready for your live demo! Good luck! 🎓🌟**

---

**Guide Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: ✅ Demo-Ready
