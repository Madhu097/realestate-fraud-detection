"""
Display Evaluation Results

This script displays the evaluation results in a readable format
"""
import pandas as pd
import os

# Load results
results_path = os.path.join(os.path.dirname(__file__), 'evaluation_results.csv')
summary_path = os.path.join(os.path.dirname(__file__), 'performance_summary.csv')

print("=" * 80)
print("  FRAUD DETECTION SYSTEM - EVALUATION RESULTS")
print("=" * 80)

# Load and display performance summary
print("\n[PERFORMANCE SUMMARY]")
summary_df = pd.read_csv(summary_path)
print(summary_df.to_string(index=False))

# Load detailed results
results_df = pd.read_csv(results_path)

print(f"\n[DATASET STATISTICS]")
print(f"  Total Listings Evaluated: {len(results_df)}")
print(f"  True Fraudulent: {(results_df['true_label'] == 1).sum()}")
print(f"  True Normal: {(results_df['true_label'] == 0).sum()}")

print(f"\n[PREDICTION STATISTICS]")
print(f"  Predicted Fraudulent: {(results_df['predicted_label'] == 1).sum()}")
print(f"  Predicted Normal: {(results_df['predicted_label'] == 0).sum()}")

# Confusion Matrix
tp = ((results_df['true_label'] == 1) & (results_df['predicted_label'] == 1)).sum()
tn = ((results_df['true_label'] == 0) & (results_df['predicted_label'] == 0)).sum()
fp = ((results_df['true_label'] == 0) & (results_df['predicted_label'] == 1)).sum()
fn = ((results_df['true_label'] == 1) & (results_df['predicted_label'] == 0)).sum()

print(f"\n[CONFUSION MATRIX]")
print("+------------------+--------------+--------------+")
print("|                  |  Predicted   |  Predicted   |")
print("|                  |   Normal     |  Fraudulent  |")
print("+------------------+--------------+--------------+")
print(f"| Actual Normal    |  {tn:10d}  |  {fp:10d}  |")
print(f"| Actual Fraud     |  {fn:10d}  |  {tp:10d}  |")
print("+------------------+--------------+--------------+")

print(f"\n  - True Negatives (TN):  {tn:4d} - Correctly identified normal listings")
print(f"  - False Positives (FP): {fp:4d} - Normal listings incorrectly flagged as fraud")
print(f"  - False Negatives (FN): {fn:4d} - Fraudulent listings missed")
print(f"  - True Positives (TP):  {tp:4d} - Correctly identified fraudulent listings")

# Calculate metrics
accuracy = (tp + tn) / len(results_df) if len(results_df) > 0 else 0
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"\n[OVERALL METRICS]")
print(f"  Accuracy:  {accuracy:.1%}")
print(f"  Precision: {precision:.1%}")
print(f"  Recall:    {recall:.1%}")
print(f"  F1-Score:  {f1:.1%}")

# Fraud type analysis
print(f"\n[FRAUD TYPE DETECTION RATES]")
fraud_types = results_df[results_df['true_label'] == 1]['fraud_type'].unique()
for fraud_type in sorted(fraud_types):
    subset = results_df[results_df['fraud_type'] == fraud_type]
    total = len(subset)
    detected = (subset['predicted_label'] == 1).sum()
    rate = detected / total if total > 0 else 0
    print(f"  {fraud_type:20s}: {detected:3d}/{total:3d} = {rate:6.1%}")

print("\n" + "=" * 80)
print(f"Results saved to:")
print(f"  - {results_path}")
print(f"  - {summary_path}")
print("=" * 80)
