# Fraud Detection System Evaluation

## Overview

This evaluation module provides comprehensive performance analysis of the hybrid AI-based real estate fraud detection system for academic submission.

## Components

### 1. `fraud_injector.py`
Synthetic fraud injection module that creates labeled evaluation datasets.

**Fraud Types Injected:**
- **Price Fraud**: Abnormally low/high prices (40-70% deviation)
- **Text Fraud**: Urgency keywords, scam patterns, exaggeration
- **Location Fraud**: Coordinate mismatches (0.5-2 degree shifts)
- **Multi-Fraud**: Combination of multiple fraud types

**Key Functions:**
- `inject_price_fraud()`: Inject price anomalies
- `inject_text_fraud()`: Inject suspicious text patterns
- `inject_location_fraud()`: Inject coordinate mismatches
- `create_synthetic_fraud_dataset()`: Generate labeled dataset

### 2. `evaluate_model.py`
Main evaluation script with comprehensive metrics and analysis.

**Evaluation Metrics:**
- ✅ Precision
- ✅ Recall
- ✅ F1-Score
- ✅ Accuracy
- ✅ ROC-AUC
- ✅ Confusion Matrix

**Analysis Provided:**
- Overall system performance
- Module-wise performance (Price, Text, Location)
- Fraud type detection rates
- Error analysis (False Positives, False Negatives)
- Performance summary tables

## Usage

### Quick Start

```bash
# Navigate to evaluation directory
cd backend/evaluation

# Run evaluation
python evaluate_model.py
```

### Expected Output

The script will:
1. Load the dataset
2. Create synthetic fraud dataset (200 normal + 200 fraudulent)
3. Run fraud detection on all listings
4. Calculate comprehensive metrics
5. Generate detailed reports

### Output Files

- `evaluation_results.csv`: Detailed results for each listing
- `performance_summary.csv`: Summary metrics for all modules

## Evaluation Dataset

### Dataset Composition

- **Total Listings**: 400
- **Normal Listings**: 200 (50%)
- **Fraudulent Listings**: 200 (50%)

### Fraud Distribution

- Price Fraud (Underpriced): 25%
- Price Fraud (Overpriced): 15%
- Text Fraud (Urgency): 20%
- Text Fraud (Scam): 15%
- Text Fraud (Exaggeration): 10%
- Location Fraud: 10%
- Multi-Fraud: 5%

## Metrics Explanation

### Precision
```
Precision = TP / (TP + FP)
```
Percentage of fraud predictions that are correct.
**High precision** = Few false alarms

### Recall
```
Recall = TP / (TP + FN)
```
Percentage of actual fraud cases detected.
**High recall** = Few missed frauds

### F1-Score
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Harmonic mean of precision and recall.
**Balanced metric** for overall performance

### Confusion Matrix

```
                 Predicted Normal  Predicted Fraud
Actual Normal         TN                FP
Actual Fraud          FN                TP
```

- **TN (True Negative)**: Correctly identified normal listings
- **FP (False Positive)**: Normal listings incorrectly flagged
- **FN (False Negative)**: Fraudulent listings missed
- **TP (True Positive)**: Correctly identified fraud

## Configuration

### Fraud Detection Threshold

```python
FRAUD_THRESHOLD = 0.5  # Overall system threshold
```

Listings with `fraud_probability >= 0.5` are classified as fraudulent.

### Module Thresholds

```python
MODULE_THRESHOLDS = {
    'price': 0.6,
    'text': 0.6,
    'location': 0.6,
    'image': 0.6
}
```

Individual module thresholds for module-wise evaluation.

### Dataset Size

```python
NUM_NORMAL_LISTINGS = 200
NUM_FRAUDULENT_LISTINGS = 200
```

Adjust these values to change evaluation dataset size.

## Academic Submission Notes

### Honesty and Transparency

✅ **Synthetic Labels**: All fraud labels are synthetically generated
✅ **No Deep Learning**: Uses rule-based and statistical methods only
✅ **Reproducible**: Same inputs produce same outputs (deterministic)
✅ **Explainable**: Clear reasoning for every decision

### Limitations

1. **Synthetic Data**: Fraud patterns are simulated, not real-world
2. **Image Module**: Not implemented (placeholder only)
3. **Dataset Size**: Limited to available real estate data
4. **Threshold Tuning**: Thresholds are manually calibrated

### Strengths

1. **Comprehensive Metrics**: Industry-standard sklearn metrics
2. **Module-wise Analysis**: Understand each component's performance
3. **Error Analysis**: Identify and analyze failure cases
4. **Fraud Type Analysis**: Track detection rates by fraud type

## Sample Output

```
================================================================================
  STEP 4: Overall System Performance
================================================================================

Performance Metrics:
┌─────────────────────┬──────────┐
│ Metric              │  Value   │
├─────────────────────┼──────────┤
│ Accuracy            │  0.8250  │
│ Precision           │  0.8100  │
│ Recall              │  0.7800  │
│ F1-Score            │  0.7947  │
│ ROC-AUC             │  0.8500  │
└─────────────────────┴──────────┘

Confusion Matrix:
┌─────────────────┬──────────────┬──────────────┐
│                 │  Predicted   │  Predicted   │
│                 │   Normal     │  Fraudulent  │
├─────────────────┼──────────────┼──────────────┤
│ Actual Normal   │         165  │          35  │
│ Actual Fraud    │          44  │         156  │
└─────────────────┴──────────────┴──────────────┘

Confusion Matrix Breakdown:
  • True Negatives (TN):   165 - Correctly identified normal listings
  • False Positives (FP):   35 - Normal listings incorrectly flagged as fraud
  • False Negatives (FN):   44 - Fraudulent listings missed
  • True Positives (TP):   156 - Correctly identified fraudulent listings
```

## Troubleshooting

### Dataset Not Found

```
❌ Error loading dataset: Dataset file not found
```

**Solution**: Ensure the dataset is properly loaded in `app/utils/data_loader.py`

### Import Errors

```
❌ ModuleNotFoundError: No module named 'sklearn'
```

**Solution**: Install required packages
```bash
pip install scikit-learn matplotlib seaborn pandas numpy
```

### Low Performance

If metrics are unexpectedly low:
1. Check fraud injection patterns
2. Verify module thresholds
3. Review fraud detection logic
4. Analyze error cases

## Future Improvements

1. **Real-world Data**: Collect actual fraud cases
2. **Image Module**: Implement image fraud detection
3. **Threshold Optimization**: Use ROC curves for optimal thresholds
4. **Cross-validation**: Implement k-fold validation
5. **Temporal Analysis**: Test on time-series data

## Contact

For questions or issues, refer to the main project documentation.

---

**Last Updated**: 2026-01-20
**Version**: 1.0.0
**Author**: Senior ML Engineer
