# Quick Demo Inputs - Copy & Paste Ready

## 🟢 NORMAL LISTING 1: Standard 2BHK

**Title**: `Spacious 2BHK Apartment in Prime Location`

**Description**: `Well-maintained 2BHK apartment with 2 bathrooms, modular kitchen, and covered parking. Located in a peaceful residential area with good connectivity to schools and hospitals.`

**Price**: `4500000`

**Area (sqft)**: `1100`

**City**: `Mumbai`

**Locality**: `Andheri West`

**Latitude**: `19.1334`

**Longitude**: `72.8291`

**Expected**: ✅ LOW fraud (0.10-0.20), No fraud types

---

## 🟢 NORMAL LISTING 2: Luxury Penthouse

**Title**: `Premium 3BHK Penthouse with Panoramic Views`

**Description**: `Luxurious penthouse featuring 3 spacious bedrooms, 3 bathrooms, imported modular kitchen, private terrace, and dedicated parking. Building amenities include swimming pool, gym, and 24/7 security.`

**Price**: `12500000`

**Area (sqft)**: `2200`

**City**: `Mumbai`

**Locality**: `Bandra West`

**Latitude**: `19.0596`

**Longitude**: `72.8295`

**Expected**: ✅ LOW fraud (0.15-0.25), No fraud types

---

## 🟢 NORMAL LISTING 3: Budget 1BHK

**Title**: `Affordable 1BHK Flat for First-Time Buyers`

**Description**: `Compact 1BHK flat ideal for bachelors or small families. Includes basic amenities, close to railway station and market. Ready to move in condition.`

**Price**: `2800000`

**Area (sqft)**: `550`

**City**: `Mumbai`

**Locality**: `Malad East`

**Latitude**: `19.1868`

**Longitude**: `72.8493`

**Expected**: ✅ LOW fraud (0.10-0.20), No fraud types

---

## 🔴 PRICE FRAUD 1: Severely Underpriced

**Title**: `3BHK Apartment in Andheri West`

**Description**: `Spacious 3BHK apartment with modern amenities, parking, and good connectivity. Well-maintained building with lift and security.`

**Price**: `1500000`

**Area (sqft)**: `1400`

**City**: `Mumbai`

**Locality**: `Andheri West`

**Latitude**: `19.1334`

**Longitude**: `72.8291`

**Expected**: 🔴 HIGH fraud (0.70-0.85), Price Fraud flagged

---

## 🔴 PRICE FRAUD 2: Overpriced

**Title**: `2BHK Flat in Malad`

**Description**: `Standard 2BHK flat with basic amenities. Suitable for families. Close to local market and transport.`

**Price**: `15000000`

**Area (sqft)**: `900`

**City**: `Mumbai`

**Locality**: `Malad East`

**Latitude**: `19.1868`

**Longitude**: `72.8493`

**Expected**: 🔴 HIGH fraud (0.60-0.75), Price Fraud flagged

---

## 🟡 TEXT FRAUD 1: Urgency + Scam Keywords

**Title**: `URGENT SALE! Don't Miss This Amazing Deal!`

**Description**: `HURRY! LIMITED TIME OFFER! This is a GUARANTEED investment opportunity. 100% SAFE and RISK-FREE property. Act now before it's gone! Cash only, advance payment required. Wire transfer accepted. This is a once in a lifetime chance!`

**Price**: `5000000`

**Area (sqft)**: `1200`

**City**: `Mumbai`

**Locality**: `Andheri West`

**Latitude**: `19.1334`

**Longitude**: `72.8291`

**Expected**: 🟡 MEDIUM-HIGH fraud (0.55-0.70), Text Fraud flagged

---

## 🟡 TEXT FRAUD 2: Excessive Exaggeration

**Title**: `ULTIMATE LUXURY PREMIUM EXCLUSIVE WORLD-CLASS Property`

**Description**: `This is the BEST, most AMAZING, INCREDIBLE, UNBELIEVABLE property you will ever find! PERFECT in every way! The most EXCLUSIVE and PREMIUM apartment in the ENTIRE city! This is GUARANTEED to be the ULTIMATE investment!`

**Price**: `8000000`

**Area (sqft)**: `1500`

**City**: `Mumbai`

**Locality**: `Bandra West`

**Latitude**: `19.0596`

**Longitude**: `72.8295`

**Expected**: 🟡 MEDIUM-HIGH fraud (0.50-0.65), Text Fraud flagged

---

## 🟠 LOCATION FRAUD: Coordinate Mismatch

**Title**: `Beautiful 2BHK Apartment in Andheri West`

**Description**: `Well-maintained apartment in prime Andheri West location. Close to metro station, schools, and shopping centers. Excellent connectivity.`

**Price**: `6500000`

**Area (sqft)**: `1100`

**City**: `Mumbai`

**Locality**: `Andheri West`

**Latitude**: `18.5204`

**Longitude**: `73.8567`

**Expected**: 🟠 MEDIUM fraud (0.50-0.65), Location Fraud flagged

**Note**: Coordinates point to Pune (~150km away), not Andheri West

---

## 🔴 MULTI-FRAUD: All Types Combined

**Title**: `URGENT! AMAZING 3BHK - ONCE IN LIFETIME DEAL!`

**Description**: `HURRY! LIMITED TIME! This GUARANTEED 100% SAFE investment is UNBELIEVABLE! The BEST property EVER! Act now, cash only, advance payment required. Don't miss this INCREDIBLE opportunity!`

**Price**: `1200000`

**Area (sqft)**: `1600`

**City**: `Mumbai`

**Locality**: `Bandra West`

**Latitude**: `18.9220`

**Longitude**: `72.8347`

**Expected**: 🔴 VERY HIGH fraud (0.80-0.95), ALL fraud types flagged

**Note**: Combines underpricing, suspicious text, and wrong coordinates

---

## 📋 Quick Reference Table

| # | Type | Price | Expected Fraud | Fraud Types |
|---|------|-------|----------------|-------------|
| 1 | Normal | ₹45L | 0.10-0.20 | None |
| 2 | Normal | ₹125L | 0.15-0.25 | None |
| 3 | Normal | ₹28L | 0.10-0.20 | None |
| 4 | Price ⬇️ | ₹15L | 0.70-0.85 | Price |
| 5 | Price ⬆️ | ₹150L | 0.60-0.75 | Price |
| 6 | Text 🚨 | ₹50L | 0.55-0.70 | Text |
| 7 | Text 💬 | ₹80L | 0.50-0.65 | Text |
| 8 | Location 📍 | ₹65L | 0.50-0.65 | Location |
| 9 | Multi 🔥 | ₹12L | 0.80-0.95 | All |

---

## 🎯 Recommended Demo Order

1. **Normal #1** (2BHK) - Show system doesn't flag legitimate listings
2. **Price Fraud #1** (Underpriced) - Show price detection
3. **Text Fraud #1** (Urgency) - Show text analysis
4. **Location Fraud** - Show coordinate verification
5. **Multi-Fraud** - Show fusion engine combining all signals

**Total Demo Time**: ~8-10 minutes

---

## ✅ Pre-Demo Checklist

- [ ] Backend running: `http://localhost:8000/health`
- [ ] Frontend running: `http://localhost:5173`
- [ ] Dataset loaded (check backend logs)
- [ ] Browser console clear (F12)
- [ ] This file open for copy-paste

---

## 🎬 Demo Script

**[Test 1 - Normal]**
"Let me start with a legitimate listing to show the system doesn't flag normal properties..."
*Copy Normal #1, submit, show LOW fraud probability*

**[Test 2 - Price Fraud]**
"Now let's test with a suspiciously underpriced property..."
*Copy Price Fraud #1, submit, show HIGH fraud probability and Price Fraud flag*

**[Test 3 - Text Fraud]**
"Here's a listing with urgency keywords and scam indicators..."
*Copy Text Fraud #1, submit, show Text Fraud detection*

**[Test 4 - Location Fraud]**
"This listing claims to be in Andheri but coordinates point elsewhere..."
*Copy Location Fraud, submit, show coordinate mismatch*

**[Test 5 - Multi-Fraud]**
"Finally, a listing with multiple fraud indicators..."
*Copy Multi-Fraud, submit, show all modules detecting fraud*

---

## 📸 Screenshot Checklist

- [ ] Normal listing result (green indicator)
- [ ] Price fraud result (red indicator)
- [ ] Text fraud result (yellow/orange indicator)
- [ ] Location fraud result
- [ ] Multi-fraud result (dark red)
- [ ] History view with all tests
- [ ] Module scores breakdown
- [ ] Fraud explanations panel

---

**Quick Reference Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: ✅ Ready for Demo
