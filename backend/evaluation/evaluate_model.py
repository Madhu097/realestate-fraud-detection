"""
Model Evaluation Script for Real Estate Fraud Detection System

This script evaluates the performance of the hybrid fraud detection system using:
- Labeled synthetic fraud dataset
- sklearn metrics (Precision, Recall, F1-score, Confusion Matrix)
- Module-wise and overall performance analysis
- Detailed performance reports

Author: Senior ML Engineer
Purpose: Academic submission and system validation
"""
import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import fraud detection modules
from app.services.price_fraud import detect_price_fraud
from app.services.text_fraud import detect_text_fraud
from app.services.location_fraud import detect_location_fraud
from app.services.fusion import fuse_fraud_signals
from app.utils.data_loader import load_dataset

# Import fraud injection module
from fraud_injector import create_synthetic_fraud_dataset, get_fraud_statistics

# Import sklearn metrics
from sklearn.metrics import (
    precision_score, recall_score, f1_score, 
    confusion_matrix, classification_report,
    accuracy_score, roc_auc_score, roc_curve
)

# For visualization
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURATION
# ============================================================

# Fraud detection threshold
FRAUD_THRESHOLD = 0.5  # Listings with fraud_probability >= 0.5 are classified as fraudulent

# Module-specific thresholds (for individual module evaluation)
MODULE_THRESHOLDS = {
    'price': 0.6,
    'text': 0.6,
    'location': 0.6,
    'image': 0.6
}

# Evaluation dataset size
NUM_NORMAL_LISTINGS = 200
NUM_FRAUDULENT_LISTINGS = 200


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_section_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subsection_header(title: str):
    """Print a formatted subsection header"""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def analyze_single_listing(listing: pd.Series, dataset: pd.DataFrame) -> Dict:
    """
    Analyze a single listing and return fraud scores
    
    Args:
        listing: Listing data
        dataset: Reference dataset for price fraud detection
        
    Returns:
        Dictionary with fraud scores and predictions
    """
    # Price fraud detection
    price_score, price_explanation = detect_price_fraud(
        listing_price=listing['price'],
        locality=listing['locality'],
        df=dataset
    )
    
    # Text fraud detection
    text_score, text_explanations = detect_text_fraud(
        title=listing['title'],
        description=listing['description'],
        save_to_corpus=False  # Don't save during evaluation
    )
    
    # Location fraud detection
    location_score, location_explanation = detect_location_fraud(
        locality=listing['locality'],
        latitude=listing['latitude'],
        longitude=listing['longitude'],
        price=listing['price']
    )
    
    # Image fraud (placeholder)
    image_score = 0.0
    image_explanation = "Image fraud detection not implemented"
    
    # Fusion
    final_fraud_probability, fraud_types, explanations = fuse_fraud_signals(
        price_score=price_score,
        price_explanation=price_explanation,
        image_score=image_score,
        image_explanation=image_explanation,
        text_score=text_score,
        text_explanations=text_explanations,
        location_score=location_score,
        location_explanation=location_explanation
    )
    
    return {
        'price_score': price_score,
        'text_score': text_score,
        'location_score': location_score,
        'image_score': image_score,
        'final_fraud_probability': final_fraud_probability,
        'fraud_types': fraud_types,
        'explanations': explanations
    }


def evaluate_dataset(eval_df: pd.DataFrame, dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluate all listings in the dataset
    
    Args:
        eval_df: Evaluation dataset with fraud labels
        dataset: Reference dataset for fraud detection
        
    Returns:
        DataFrame with predictions and scores
    """
    print_subsection_header("Analyzing Listings")
    print(f"Total listings to analyze: {len(eval_df)}")
    
    results = []
    errors = 0
    
    for idx, row in eval_df.iterrows():
        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1}/{len(eval_df)} listings...")
        
        try:
            # Analyze listing
            analysis = analyze_single_listing(row, dataset)
            
            # Store results
            result = {
                'listing_id': idx,
                'true_label': row['fraud_label'],
                'fraud_type': row['fraud_type'],
                'fraud_details': row['fraud_details'],
                'price_score': analysis['price_score'],
                'text_score': analysis['text_score'],
                'location_score': analysis['location_score'],
                'image_score': analysis['image_score'],
                'final_fraud_probability': analysis['final_fraud_probability'],
                'predicted_label': 1 if analysis['final_fraud_probability'] >= FRAUD_THRESHOLD else 0,
                'detected_fraud_types': ', '.join(analysis['fraud_types']) if analysis['fraud_types'] else 'None'
            }
            
            results.append(result)
            
        except Exception as e:
            errors += 1
            print(f"\n  [ERROR] Failed to analyze listing {idx}: {str(e)}")
            if errors <= 3:  # Show details for first 3 errors
                import traceback
                traceback.print_exc()
            if errors > 10:  # Stop if too many errors
                print(f"\n  [FATAL] Too many errors ({errors}), stopping evaluation")
                break
    
    print(f"  [OK] Completed analysis of {len(results)} listings ({errors} errors)")
    
    return pd.DataFrame(results)



def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> Dict:
    """
    Calculate comprehensive evaluation metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_prob: Predicted probabilities
        
    Returns:
        Dictionary with all metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0),
        'confusion_matrix': confusion_matrix(y_true, y_pred),
    }
    
    # Add ROC-AUC if we have both classes
    if len(np.unique(y_true)) > 1:
        metrics['roc_auc'] = roc_auc_score(y_true, y_prob)
    else:
        metrics['roc_auc'] = None
    
    return metrics


def print_confusion_matrix(cm: np.ndarray):
    """
    Print confusion matrix in a formatted table
    
    Args:
        cm: Confusion matrix
    """
    print("\nConfusion Matrix:")
    print("+------------------+--------------+--------------+")
    print("|                  |  Predicted   |  Predicted   |")
    print("|                  |   Normal     |  Fraudulent  |")
    print("+------------------+--------------+--------------+")
    print(f"| Actual Normal    |  {cm[0][0]:10d}  |  {cm[0][1]:10d}  |")
    print(f"| Actual Fraud     |  {cm[1][0]:10d}  |  {cm[1][1]:10d}  |")
    print("+------------------+--------------+--------------+")
    
    # Calculate derived metrics
    tn, fp, fn, tp = cm.ravel()
    
    print("\nConfusion Matrix Breakdown:")
    print(f"  - True Negatives (TN):  {tn:4d} - Correctly identified normal listings")
    print(f"  - False Positives (FP): {fp:4d} - Normal listings incorrectly flagged as fraud")
    print(f"  - False Negatives (FN): {fn:4d} - Fraudulent listings missed")
    print(f"  - True Positives (TP):  {tp:4d} - Correctly identified fraudulent listings")


def print_metrics_table(metrics: Dict):
    """
    Print metrics in a formatted table
    
    Args:
        metrics: Dictionary with metrics
    """
    print("\nPerformance Metrics:")
    print("+---------------------+----------+")
    print("| Metric              |  Value   |")
    print("+---------------------+----------+")
    print(f"| Accuracy            |  {metrics['accuracy']:.4f}  |")
    print(f"| Precision           |  {metrics['precision']:.4f}  |")
    print(f"| Recall              |  {metrics['recall']:.4f}  |")
    print(f"| F1-Score            |  {metrics['f1_score']:.4f}  |")
    if metrics['roc_auc'] is not None:
        print(f"| ROC-AUC             |  {metrics['roc_auc']:.4f}  |")
    print("+---------------------+----------+")



def evaluate_module_performance(results_df: pd.DataFrame, module_name: str, threshold: float) -> Dict:
    """
    Evaluate performance of a single fraud detection module
    
    Args:
        results_df: Results DataFrame
        module_name: Name of the module ('price', 'text', 'location', 'image')
        threshold: Classification threshold for this module
        
    Returns:
        Dictionary with module metrics
    """
    score_column = f'{module_name}_score'
    
    # Get true labels and predictions
    y_true = results_df['true_label'].values
    y_prob = results_df[score_column].values
    y_pred = (y_prob >= threshold).astype(int)
    
    # Calculate metrics
    metrics = calculate_metrics(y_true, y_pred, y_prob)
    
    return metrics


def analyze_error_cases(results_df: pd.DataFrame, error_type: str = 'false_positive', max_cases: int = 5):
    """
    Analyze and display error cases
    
    Args:
        results_df: Results DataFrame
        error_type: Type of error ('false_positive' or 'false_negative')
        max_cases: Maximum number of cases to display
    """
    if error_type == 'false_positive':
        # Normal listings incorrectly flagged as fraud
        errors = results_df[(results_df['true_label'] == 0) & (results_df['predicted_label'] == 1)]
        title = "False Positives (Normal listings flagged as fraud)"
    else:
        # Fraudulent listings missed
        errors = results_df[(results_df['true_label'] == 1) & (results_df['predicted_label'] == 0)]
        title = "False Negatives (Fraudulent listings missed)"
    
    print(f"\n{title}:")
    print(f"Total: {len(errors)}")
    
    if len(errors) > 0:
        print(f"\nShowing first {min(max_cases, len(errors))} cases:")
        for idx, (_, row) in enumerate(errors.head(max_cases).iterrows(), 1):
            print(f"\n  Case {idx}:")
            print(f"    Fraud Type: {row['fraud_type']}")
            print(f"    Fraud Details: {row['fraud_details']}")
            print(f"    Final Probability: {row['final_fraud_probability']:.3f}")
            print(f"    Module Scores: Price={row['price_score']:.3f}, Text={row['text_score']:.3f}, Location={row['location_score']:.3f}")


def create_performance_summary_df(overall_metrics: Dict, module_metrics: Dict) -> pd.DataFrame:
    """
    Create a summary DataFrame for easy visualization
    
    Args:
        overall_metrics: Overall system metrics
        module_metrics: Dictionary of module-wise metrics
        
    Returns:
        Summary DataFrame
    """
    summary_data = []
    
    # Overall system
    summary_data.append({
        'Module': 'Overall System',
        'Precision': overall_metrics['precision'],
        'Recall': overall_metrics['recall'],
        'F1-Score': overall_metrics['f1_score'],
        'Accuracy': overall_metrics['accuracy']
    })
    
    # Individual modules
    for module_name, metrics in module_metrics.items():
        summary_data.append({
            'Module': module_name.capitalize(),
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1-Score': metrics['f1_score'],
            'Accuracy': metrics['accuracy']
        })
    
    return pd.DataFrame(summary_data)


# ============================================================
# MAIN EVALUATION FUNCTION
# ============================================================

def main():
    """
    Main evaluation function
    """
    print_section_header("REAL ESTATE FRAUD DETECTION SYSTEM - EVALUATION")
    print(f"Evaluation started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ============================================================
    # STEP 1: Load Dataset
    # ============================================================
    print_section_header("STEP 1: Loading Dataset")
    
    try:
        dataset = load_dataset()
        print(f"✅ Dataset loaded successfully: {len(dataset)} properties")
        print(f"   Columns: {', '.join(dataset.columns.tolist())}")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    # ============================================================
    # STEP 2: Create Synthetic Fraud Dataset
    # ============================================================
    print_section_header("STEP 2: Creating Synthetic Fraud Dataset")
    
    print("Generating labeled evaluation dataset...")
    print(f"  • Normal listings: {NUM_NORMAL_LISTINGS}")
    print(f"  • Fraudulent listings: {NUM_FRAUDULENT_LISTINGS}")
    
    try:
        eval_df = create_synthetic_fraud_dataset(
            df=dataset,
            num_fraudulent=NUM_FRAUDULENT_LISTINGS
        )
        print(f"✅ Evaluation dataset created: {len(eval_df)} listings")
        
        # Get fraud statistics
        fraud_stats = get_fraud_statistics(eval_df)
        print("\nDataset Statistics:")
        print(f"  • Total listings: {fraud_stats['total_listings']}")
        print(f"  • Normal listings: {fraud_stats['normal_listings']}")
        print(f"  • Fraudulent listings: {fraud_stats['fraudulent_listings']}")
        print(f"  • Fraud percentage: {fraud_stats['fraud_percentage']:.1f}%")
        print("\nFraud Type Distribution:")
        for fraud_type, count in fraud_stats['fraud_type_distribution'].items():
            print(f"  • {fraud_type}: {count}")
        
    except Exception as e:
        print(f"❌ Error creating evaluation dataset: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ============================================================
    # STEP 3: Run Fraud Detection on Evaluation Dataset
    # ============================================================
    print_section_header("STEP 3: Running Fraud Detection")
    
    try:
        results_df = evaluate_dataset(eval_df, dataset)
        print(f"✅ Fraud detection completed")
        
        # Save results
        results_path = os.path.join(os.path.dirname(__file__), 'evaluation_results.csv')
        results_df.to_csv(results_path, index=False)
        print(f"   Results saved to: {results_path}")
        
    except Exception as e:
        print(f"❌ Error during fraud detection: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ============================================================
    # STEP 4: Calculate Overall Performance Metrics
    # ============================================================
    print_section_header("STEP 4: Overall System Performance")
    
    y_true = results_df['true_label'].values
    y_pred = results_df['predicted_label'].values
    y_prob = results_df['final_fraud_probability'].values
    
    overall_metrics = calculate_metrics(y_true, y_pred, y_prob)
    
    print_metrics_table(overall_metrics)
    print_confusion_matrix(overall_metrics['confusion_matrix'])
    
    # ============================================================
    # STEP 5: Module-wise Performance Analysis
    # ============================================================
    print_section_header("STEP 5: Module-wise Performance Analysis")
    
    module_metrics = {}
    
    for module_name, threshold in MODULE_THRESHOLDS.items():
        if module_name == 'image':
            continue  # Skip image module (not implemented)
        
        print_subsection_header(f"{module_name.upper()} Fraud Detection Module")
        
        metrics = evaluate_module_performance(results_df, module_name, threshold)
        module_metrics[module_name] = metrics
        
        print_metrics_table(metrics)
        print_confusion_matrix(metrics['confusion_matrix'])
    
    # ============================================================
    # STEP 6: Performance Summary
    # ============================================================
    print_section_header("STEP 6: Performance Summary")
    
    summary_df = create_performance_summary_df(overall_metrics, module_metrics)
    
    print("\nPerformance Summary (All Modules):")
    print(summary_df.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
    
    # Save summary
    summary_path = os.path.join(os.path.dirname(__file__), 'performance_summary.csv')
    summary_df.to_csv(summary_path, index=False)
    print(f"\n✅ Summary saved to: {summary_path}")
    
    # ============================================================
    # STEP 7: Error Analysis
    # ============================================================
    print_section_header("STEP 7: Error Analysis")
    
    analyze_error_cases(results_df, 'false_positive', max_cases=3)
    analyze_error_cases(results_df, 'false_negative', max_cases=3)
    
    # ============================================================
    # STEP 8: Fraud Type Analysis
    # ============================================================
    print_section_header("STEP 8: Fraud Type Detection Analysis")
    
    # Analyze how well we detect each fraud type
    fraud_type_performance = {}
    
    for fraud_type in eval_df[eval_df['fraud_label'] == 1]['fraud_type'].unique():
        subset = results_df[results_df['fraud_type'] == fraud_type]
        if len(subset) > 0:
            y_true_subset = subset['true_label'].values
            y_pred_subset = subset['predicted_label'].values
            
            detected = (y_pred_subset == 1).sum()
            total = len(subset)
            detection_rate = detected / total if total > 0 else 0
            
            fraud_type_performance[fraud_type] = {
                'total': total,
                'detected': detected,
                'detection_rate': detection_rate
            }
    
    print("\nFraud Type Detection Rates:")
    print("+---------------------+-------+----------+----------------+")
    print("| Fraud Type          | Total | Detected | Detection Rate |")
    print("+---------------------+-------+----------+----------------+")
    for fraud_type, perf in fraud_type_performance.items():
        print(f"| {fraud_type:19s} | {perf['total']:5d} | {perf['detected']:8d} | {perf['detection_rate']:13.1%} |")
    print("+---------------------+-------+----------+----------------+")
    
    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print_section_header("EVALUATION COMPLETE")
    
    print("\n[KEY FINDINGS]")
    print(f"  - Overall Accuracy:  {overall_metrics['accuracy']:.1%}")
    print(f"  - Overall Precision: {overall_metrics['precision']:.1%}")
    print(f"  - Overall Recall:    {overall_metrics['recall']:.1%}")
    print(f"  - Overall F1-Score:  {overall_metrics['f1_score']:.1%}")
    
    if overall_metrics['roc_auc'] is not None:
        print(f"  - ROC-AUC Score:     {overall_metrics['roc_auc']:.1%}")
    
    print("\n[OUTPUT FILES]")
    print(f"  - Detailed results: {results_path}")
    print(f"  - Performance summary: {summary_path}")
    
    print(f"\n[OK] Evaluation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 80)

    
    # Return results for programmatic access
    return {
        'overall_metrics': overall_metrics,
        'module_metrics': module_metrics,
        'results_df': results_df,
        'summary_df': summary_df,
        'fraud_type_performance': fraud_type_performance
    }


if __name__ == "__main__":
    main()
