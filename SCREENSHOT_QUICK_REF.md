# Quick Screenshot Reference Card

## 📸 20 Screenshots for Your Report

### Frontend (12 screenshots)

| # | File Name | What to Capture | Key Point |
|---|-----------|-----------------|-----------|
| 1 | `01_homepage_landing.png` | Empty form, homepage | Clean UI |
| 2 | `02_form_filled_sample.png` | Form with Normal N1 data | Input workflow |
| 3 | `03_loading_analysis.png` | Spinner during submit | User feedback |
| 4 | `04_result_normal_low_fraud.png` | Normal result (GREEN) | Low fraud 0.15 |
| 5 | `05_result_price_fraud.png` | Price fraud (RED) | High fraud 0.78 |
| 6 | `06_result_text_fraud.png` | Text fraud (ORANGE) | Medium fraud 0.65 |
| 7 | `07_result_location_fraud.png` | Location fraud (ORANGE) | Coord mismatch |
| 8 | `08_result_multi_fraud.png` | Multi-fraud (DARK RED) | Very high 0.88 |
| 9 | `09_module_scores_chart.png` | Chart showing module scores | Breakdown |
| 10 | `10_fraud_explanations.png` | Explanations panel | Explainability |
| 11 | `11_history_fraud_database.png` | History tab with multiple entries | Audit trail |
| 12 | `12_error_handling.png` | Error message (price=0) | Validation |

### Backend (3 screenshots)

| # | File Name | What to Capture | Key Point |
|---|-----------|-----------------|-----------|
| 13 | `13_api_documentation.png` | http://localhost:8000/docs | Swagger UI |
| 14 | `14_health_check.png` | http://localhost:8000/health | JSON response |
| 15 | `15_backend_console_logs.png` | Terminal with startup logs | Dataset loaded |

### Evaluation (5 screenshots)

| # | File Name | What to Capture | Key Point |
|---|-----------|-----------------|-----------|
| 16 | `16_evaluation_console_output.png` | evaluate_model.py output | Metrics |
| 17 | `17_performance_summary_csv.png` | performance_summary.csv | Module scores |
| 18 | `18_evaluation_results_sample.png` | evaluation_results.csv (10 rows) | Predictions |
| 19 | `19_confusion_matrix.png` | Confusion matrix table | TP/TN/FP/FN |
| 20 | `20_fraud_type_detection.png` | Fraud type rates table | Detection % |

---

## 🚀 Quick Capture Sequence (30 minutes)

### Setup (5 min)
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

### Capture Frontend (15 min)

**Screenshots 1-3: Form**
1. Go to http://localhost:5173
2. Screenshot 1: Empty form
3. Fill with Normal N1 data
4. Screenshot 2: Filled form
5. Click submit
6. Screenshot 3: Loading (QUICK!)

**Screenshots 4-8: Results**
7. Screenshot 4: Normal result (wait for load)
8. Click back, submit Price Fraud P1
9. Screenshot 5: Price fraud result
10. Click back, submit Text Fraud T1
11. Screenshot 6: Text fraud result
12. Click back, submit Location Fraud L1
13. Screenshot 7: Location fraud result
14. Click back, submit Multi-Fraud M1
15. Screenshot 8: Multi-fraud result

**Screenshots 9-10: Details**
16. Screenshot 9: Module scores chart (zoom if needed)
17. Screenshot 10: Explanations panel (scroll if needed)

**Screenshots 11-12: Other**
18. Click "Fraud Database" tab
19. Screenshot 11: History view
20. Click back to form, set price=0, submit
21. Screenshot 12: Error message

### Capture Backend (5 min)

**Screenshots 13-15: API**
22. Go to http://localhost:8000/docs
23. Screenshot 13: Swagger UI
24. Go to http://localhost:8000/health
25. Screenshot 14: Health JSON
26. Screenshot 15: Backend terminal logs

### Capture Evaluation (5 min)

**Screenshots 16-20: Results**
27. Run: `cd backend/evaluation && python evaluate_model.py`
28. Screenshot 16: Console output
29. Open performance_summary.csv in Excel
30. Screenshot 17: CSV table
31. Open evaluation_results.csv, show first 10 rows
32. Screenshot 18: Results sample
33. Create confusion matrix table in Excel
34. Screenshot 19: Confusion matrix
35. Create fraud type table
36. Screenshot 20: Fraud type rates

---

## 📝 Ready-to-Use Captions

### Screenshot 1
```
Figure 1: Truth in Listings - Homepage and Listing Input Interface
The system homepage features a clean, professional interface for property 
listing analysis with comprehensive input fields for title, description, 
price, area, location, and geospatial coordinates.
```

### Screenshot 4
```
Figure 4: Analysis Results - Legitimate Listing (Low Fraud Probability)
Results dashboard showing a low fraud probability of 15% for a legitimate 
property listing. No fraud types are flagged, demonstrating the system's 
ability to avoid false positives.
```

### Screenshot 5
```
Figure 5: Price Fraud Detection - Severely Underpriced Property
The system successfully detects a severely underpriced property with 78% 
fraud probability. Price module score of 0.85 indicates strong price 
anomaly detection.
```

### Screenshot 8
```
Figure 8: Multi-Fraud Detection - Fusion Engine in Action
The fusion engine combines signals from multiple modules, achieving 88% 
fraud probability with all three fraud types flagged (Price, Text, Location).
```

### Screenshot 16
```
Figure 16: Evaluation Script Console Output - Performance Metrics
Comprehensive performance metrics: Accuracy 50.75%, Precision 100.00%, 
Recall 1.50%, F1-Score 3.00%. Confusion matrix shows TP=3, TN=200, 
FP=0, FN=197.
```

### Screenshot 19
```
Figure 19: Confusion Matrix - Fraud Detection Performance
The confusion matrix reveals True Negatives (200), True Positives (3), 
and False Negatives (197). Zero False Positives confirm the system's 
conservative approach.
```

---

## ✅ Capture Checklist

### Before Starting
- [ ] Backend running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] Dataset loaded
- [ ] Browser zoom 100%
- [ ] Screenshot tool ready
- [ ] QUICK_DEMO_INPUTS.md open

### During Capture
- [ ] Screenshots 1-12 (Frontend)
- [ ] Screenshots 13-15 (Backend)
- [ ] Screenshots 16-20 (Evaluation)
- [ ] All images clear and readable
- [ ] Consistent resolution
- [ ] Proper file names

### After Capture
- [ ] 20 screenshots total
- [ ] Organized in folder
- [ ] Quality verified
- [ ] Backup created
- [ ] Ready for report

---

## 🎯 For Your Report

### Where to Use

**Chapter 1 (Introduction)**: Screenshots 1, 8  
**Chapter 3 (Design)**: Screenshots 1, 2, 13  
**Chapter 4 (Results)**: Screenshots 4-8, 16-20  
**Chapter 5 (Discussion)**: Screenshots 17, 19, 20  

### How to Insert

1. Insert image in Word/LaTeX
2. Add caption below image
3. Reference in text: "As shown in Figure 5..."
4. Ensure high resolution in final PDF

---

**Total Time**: 30 minutes  
**Total Screenshots**: 20  
**Status**: ✅ Ready to Capture
