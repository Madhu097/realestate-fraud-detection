# Quick Start Guide - Fraud Detection Evaluation

## Overview
This guide helps you quickly run the fraud detection system evaluation for academic submission.

## Prerequisites
```bash
pip install pandas numpy scikit-learn
```

## Quick Run (3 Steps)

### Step 1: Navigate to Evaluation Directory
```bash
cd backend/evaluation
```

### Step 2: Run Evaluation
```bash
python evaluate_model.py
```

**Expected Runtime**: 2-5 minutes for 400 listings

### Step 3: View Results
```bash
python display_results.py
```

## What Gets Generated

### 1. Console Output
- Dataset statistics
- Progress updates
- Performance metrics
- Confusion matrix
- Module-wise analysis
- Fraud type detection rates

### 2. Output Files

#### `evaluation_results.csv`
Detailed results for each listing:
- listing_id
- true_label (0=normal, 1=fraud)
- predicted_label
- fraud_type
- fraud_details
- price_score, text_score, location_score
- final_fraud_probability
- detected_fraud_types

#### `performance_summary.csv`
Summary metrics:
```
Module,Precision,Recall,F1-Score,Accuracy
Overall System,0.45,0.42,0.43,0.55
Price,0.35,0.42,0.38,0.52
Text,0.05,0.08,0.06,0.48
Location,0.50,0.12,0.20,0.54
```

## Understanding the Results

### Confusion Matrix
```
                 Predicted Normal  Predicted Fraud
Actual Normal         TN                FP
Actual Fraud          FN                TP
```

- **TN (True Negative)**: Normal listings correctly identified
- **FP (False Positive)**: Normal listings incorrectly flagged
- **FN (False Negative)**: Fraudulent listings missed
- **TP (True Positive)**: Fraudulent listings correctly detected

### Metrics Explained

**Precision** = TP / (TP + FP)
- "Of all fraud predictions, how many were correct?"
- High precision = Few false alarms

**Recall** = TP / (TP + FN)
- "Of all actual frauds, how many did we detect?"
- High recall = Few missed frauds

**F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)
- Balanced metric combining precision and recall

**Accuracy** = (TP + TN) / Total
- Overall correctness

## Customization

### Change Dataset Size
Edit `evaluate_model.py`:
```python
NUM_NORMAL_LISTINGS = 200      # Change this
NUM_FRAUDULENT_LISTINGS = 200  # Change this
```

### Change Fraud Threshold
Edit `evaluate_model.py`:
```python
FRAUD_THRESHOLD = 0.5  # Listings >= 0.5 are classified as fraud
```

Lower threshold = More fraud detected (higher recall, lower precision)
Higher threshold = Fewer false alarms (higher precision, lower recall)

### Change Module Thresholds
Edit `evaluate_model.py`:
```python
MODULE_THRESHOLDS = {
    'price': 0.6,      # Adjust these
    'text': 0.6,
    'location': 0.6,
}
```

## Troubleshooting

### Error: Dataset not found
**Solution**: Ensure `app/data/real_estate.csv` exists
```bash
cd backend
ls app/data/real_estate.csv
```

### Error: Module not found
**Solution**: Install required packages
```bash
pip install pandas numpy scikit-learn
```

### Low Performance
**Expected**: This is a rule-based system with synthetic fraud
- Precision: 40-50%
- Recall: 35-45%
- F1-Score: 40-50%

This is normal for:
- Synthetic fraud data
- Rule-based detection
- No machine learning training

## For Academic Submission

### What to Include

1. **Code Files**:
   - `fraud_injector.py`
   - `evaluate_model.py`
   - `display_results.py`

2. **Output Files**:
   - `evaluation_results.csv`
   - `performance_summary.csv`

3. **Documentation**:
   - `README.md`
   - `EVALUATION_REPORT.md`

4. **Screenshots**:
   - Console output showing metrics
   - Confusion matrix
   - Performance summary table

### Key Points to Mention

✅ **Honest about synthetic data**: All fraud labels are synthetically generated
✅ **No deep learning**: Uses rule-based and statistical methods
✅ **Explainable**: Every decision has clear reasoning
✅ **Reproducible**: Same inputs produce same outputs
✅ **Standard metrics**: Uses sklearn for industry-standard evaluation

### Limitations to Acknowledge

⚠️ Synthetic fraud may not represent real-world patterns
⚠️ Image module not implemented
⚠️ Text detection needs improvement
⚠️ Thresholds manually calibrated, not optimized
⚠️ Limited to available real estate data

## Next Steps

1. Run evaluation: `python evaluate_model.py`
2. View results: `python display_results.py`
3. Take screenshots of output
4. Read `EVALUATION_REPORT.md` for detailed analysis
5. Include all files in academic submission

## Support

For questions or issues:
1. Check `README.md` in evaluation folder
2. Review `EVALUATION_REPORT.md` for detailed methodology
3. Examine code comments in `evaluate_model.py`

---

**Last Updated**: 2026-01-20
**Version**: 1.0.0
**Status**: Ready for Academic Submission
