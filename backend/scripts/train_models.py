"""
Training Pipeline for Real Estate Price Prediction and Fraud Classification
Trains:
1. High-Precision Price Prediction Model (GradientBoosting / RandomForest) -> price_predictor_model.pkl
2. Locality Price-per-sqft Statistics -> locality_price_stats.pkl
3. Hybrid ExtraTree + ANN Fraud Classification Model -> hybrid_extra_tree_ann1.pkl
4. Model Metrics and Artifacts -> model_metrics.json
"""
import os
import json
import math
import pickle
import joblib
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, ExtraTreesClassifier, RandomForestRegressor, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Urgency and scam patterns for text fraud feature extraction
SCAM_KEYWORDS = [
    'wire transfer', 'western union', 'cash advance', 'advance payment', 'token money',
    'deposit now', 'urgent sale', 'distress sale', 'hurry up', 'limited time offer',
    'owner abroad', 'transfer money', 'cannot visit', 'no questions asked', '100% guaranteed'
]

def load_and_prepare_datasets():
    """Load, combine, and clean real estate datasets"""
    print("Loading datasets...")
    
    # 1. Hyderabad Data
    hyd_file = DATA_DIR / "hyderabad_real_estate.csv"
    if hyd_file.exists():
        df_hyd = pd.read_csv(hyd_file)
        if 'City' not in df_hyd.columns:
            df_hyd['City'] = 'Hyderabad'
    else:
        df_hyd = pd.DataFrame()
        
    # 2. Mumbai Data
    mum_file = DATA_DIR / "real_estate.csv"
    if mum_file.exists():
        df_mum = pd.read_csv(mum_file)
        if 'City' not in df_mum.columns:
            df_mum['City'] = 'Mumbai'
        if 'Locality' not in df_mum.columns and 'Location' in df_mum.columns:
            df_mum['Locality'] = df_mum['Location']
    else:
        df_mum = pd.DataFrame()

    # 3. Existing India dataset
    india_file = DATA_DIR / "india_real_estate.csv"
    if india_file.exists():
        df_ind = pd.read_csv(india_file)
    else:
        df_ind = pd.DataFrame()

    # Load locality coordinates mapping
    coords_file = DATA_DIR / "locality_coordinates.json"
    coords_dict = {}
    if coords_file.exists():
        try:
            with open(coords_file, 'r', encoding='utf-8') as f:
                raw_coords = json.load(f)
                for item in raw_coords:
                    key = f"{item.get('city', '').lower().strip()}|{item.get('locality', '').lower().strip()}"
                    coords_dict[key] = (item.get('latitude', 19.076), item.get('longitude', 72.877))
                    coords_dict[item.get('locality', '').lower().strip()] = (item.get('latitude', 19.076), item.get('longitude', 72.877))
        except Exception as e:
            print(f"Error loading locality coordinates: {e}")

    # Combine datasets
    dfs = [df for df in [df_hyd, df_mum, df_ind] if not df.empty]
    if not dfs:
        raise FileNotFoundError("No datasets found to train on.")
        
    combined = pd.concat(dfs, ignore_index=True)
    
    # Standardize columns
    if 'Location' in combined.columns and 'Locality' not in combined.columns:
        combined['Locality'] = combined['Location']
    elif 'Locality' in combined.columns and 'Location' not in combined.columns:
        combined['Location'] = combined['Locality']
        
    if 'No. of Bedrooms' in combined.columns and 'Bedrooms' not in combined.columns:
        combined['Bedrooms'] = combined['No. of Bedrooms']
    elif 'Bedrooms' not in combined.columns:
        combined['Bedrooms'] = 2
        
    # Clean numerical columns
    combined['Price'] = pd.to_numeric(combined['Price'], errors='coerce')
    combined['Area'] = pd.to_numeric(combined['Area'], errors='coerce')
    combined['Bedrooms'] = pd.to_numeric(combined['Bedrooms'], errors='coerce').fillna(2)
    
    # Remove NaN or unreasonable values
    combined = combined.dropna(subset=['Price', 'Area', 'Locality', 'City'])
    combined = combined[(combined['Price'] >= 300000) & (combined['Price'] <= 500000000)]
    combined = combined[(combined['Area'] >= 200) & (combined['Area'] <= 15000)]
    
    # Ensure latitude and longitude
    if 'Latitude' not in combined.columns or 'Longitude' not in combined.columns:
        combined['Latitude'] = 17.42
        combined['Longitude'] = 78.47

    # Fill missing coordinates using coords_dict or city defaults
    for idx, row in combined.iterrows():
        lat = row.get('Latitude')
        lon = row.get('Longitude')
        if pd.isna(lat) or pd.isna(lon) or (lat == 0 and lon == 0):
            loc_key = f"{str(row['City']).lower().strip()}|{str(row['Locality']).lower().strip()}"
            if loc_key in coords_dict:
                combined.at[idx, 'Latitude'] = coords_dict[loc_key][0] + np.random.uniform(-0.01, 0.01)
                combined.at[idx, 'Longitude'] = coords_dict[loc_key][1] + np.random.uniform(-0.01, 0.01)
            elif str(row['City']).lower() == 'hyderabad':
                combined.at[idx, 'Latitude'] = 17.42 + np.random.uniform(-0.05, 0.05)
                combined.at[idx, 'Longitude'] = 78.45 + np.random.uniform(-0.05, 0.05)
            else: # Mumbai
                combined.at[idx, 'Latitude'] = 19.10 + np.random.uniform(-0.08, 0.08)
                combined.at[idx, 'Longitude'] = 72.88 + np.random.uniform(-0.05, 0.05)

    combined['Price_Per_Sqft'] = combined['Price'] / combined['Area']
    
    # Save combined dataset to india_real_estate.csv
    combined.to_csv(DATA_DIR / "india_real_estate.csv", index=False)
    print(f"Loaded and prepared {len(combined)} clean properties.")
    return combined

def train_price_predictor(df):
    """Train high-accuracy GradientBoosting/RandomForest regression model to predict fair market property price"""
    print("\n--- Training Fair Market Price Prediction Model ---")
    
    # Precompute locality statistics (Median & IQR of price per sqft for every locality and city)
    locality_stats = {}
    for (city, loc), group in df.groupby(['City', 'Locality']):
        pps = group['Price_Per_Sqft'].values
        median_pps = float(np.median(pps))
        q1_pps = float(np.percentile(pps, 25))
        q3_pps = float(np.percentile(pps, 75))
        std_pps = float(np.std(pps)) if len(pps) > 1 else median_pps * 0.15
        key = f"{city.lower().strip()}|{loc.lower().strip()}"
        locality_stats[key] = {
            'city': city,
            'locality': loc,
            'median_pps': median_pps,
            'q1_pps': q1_pps,
            'q3_pps': q3_pps,
            'std_pps': std_pps if std_pps > 0 else median_pps * 0.15,
            'count': len(group)
        }
        locality_stats[loc.lower().strip()] = locality_stats[key]
        
    # City-level fallbacks
    city_stats = {}
    for city, group in df.groupby('City'):
        pps = group['Price_Per_Sqft'].values
        city_stats[city.lower().strip()] = {
            'median_pps': float(np.median(pps)),
            'std_pps': float(np.std(pps)),
            'count': len(group)
        }
    
    # Save locality stats
    joblib.dump({
        'locality_stats': locality_stats,
        'city_stats': city_stats,
        'overall_median_pps': float(df['Price_Per_Sqft'].median())
    }, MODELS_DIR / "locality_price_stats.pkl")
    print(f"Saved price-per-sqft statistics for {len(locality_stats)} localities/aliases.")

    # Prepare features for Price Regression
    # We predict log(Price) using Area, Bedrooms, Latitude, Longitude, and Locality's baseline price-per-sqft
    X_reg = []
    y_reg = []
    
    for _, row in df.iterrows():
        city_k = str(row['City']).lower().strip()
        loc_k = str(row['Locality']).lower().strip()
        full_k = f"{city_k}|{loc_k}"
        
        base_pps = locality_stats.get(full_k, {}).get('median_pps') or city_stats.get(city_k, {}).get('median_pps') or df['Price_Per_Sqft'].median()
        
        feat = [
            float(row['Area']),
            float(row['Bedrooms']),
            float(row['Latitude']),
            float(row['Longitude']),
            float(base_pps),
            float(row['Area'] * base_pps) # Baseline estimated price
        ]
        X_reg.append(feat)
        y_reg.append(np.log1p(row['Price']))
        
    X_reg = np.array(X_reg)
    y_reg = np.array(y_reg)
    
    X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.15, random_state=42)
    
    # Train GradientBoostingRegressor
    price_model = GradientBoostingRegressor(
        n_estimators=180,
        learning_rate=0.08,
        max_depth=6,
        subsample=0.85,
        random_state=42
    )
    price_model.fit(X_train, y_train)
    
    # Evaluate
    preds_log = price_model.predict(X_test)
    preds = np.expm1(preds_log)
    actuals = np.expm1(y_test)
    
    r2 = r2_score(actuals, preds)
    mae = mean_absolute_error(actuals, preds)
    mape = np.mean(np.abs((actuals - preds) / actuals)) * 100
    
    print(f"Price Predictor Model Performance:")
    print(f"  R2 Score: {r2:.4f}")
    print(f"  Mean Absolute Error: INR {mae:,.0f}")
    print(f"  MAPE: {mape:.2f}%")
    
    joblib.dump(price_model, MODELS_DIR / "price_predictor_model.pkl")
    print(f"Saved price predictor model to {MODELS_DIR / 'price_predictor_model.pkl'}")
    
    return price_model, locality_stats, city_stats, r2, mape

def generate_fraud_classification_dataset(df, price_model, locality_stats, city_stats):
    """
    Generate synthetic balanced fraud dataset grounded in real estate economics:
    Real listings vs Scam/Fraud listings (Price fraud, location mismatch, phishing urgency, spec impossibilities)
    """
    print("\n--- Generating Balanced Training Data for Fraud Classifier ---")
    
    overall_pps = df['Price_Per_Sqft'].median()
    X = []
    y = [] # 0 = Real, 1 = Fake/Fraud
    
    # 1. Real Listings (Legitimate)
    for _, row in df.iterrows():
        area = float(row['Area'])
        bedrooms = float(row['Bedrooms'])
        lat = float(row['Latitude'])
        lon = float(row['Longitude'])
        actual_price = float(row['Price'])
        
        city_k = str(row['City']).lower().strip()
        loc_k = str(row['Locality']).lower().strip()
        full_k = f"{city_k}|{loc_k}"
        
        base_pps = locality_stats.get(full_k, {}).get('median_pps') or city_stats.get(city_k, {}).get('median_pps') or overall_pps
        pred_fair_log = price_model.predict([[area, bedrooms, lat, lon, base_pps, area * base_pps]])[0]
        fair_price = np.expm1(pred_fair_log)
        
        price_ratio = actual_price / max(fair_price, 1000)
        pps = actual_price / area
        loc_std = locality_stats.get(full_k, {}).get('std_pps', base_pps * 0.2)
        pps_zscore = abs(pps - base_pps) / max(loc_std, 100)
        
        # Real listings have close distance (< 2-3 km), low urgency keywords, realistic specs
        dist_km = np.random.uniform(0.1, 2.5)
        urgency_kw = 0 if np.random.rand() > 0.1 else 1
        scam_kw = 0
        area_per_bed = area / max(bedrooms, 1)
        is_coord_out = 0
        
        feature_vector = [
            price_ratio,        # Price / Fair Price (around 0.8 - 1.25 for real)
            pps_zscore,         # Deviation from locality standard
            dist_km,            # Distance from locality center
            area,               # Floor area
            bedrooms,           # Bedrooms
            area_per_bed,       # Area per bedroom
            urgency_kw,         # Urgency keyword count
            scam_kw,            # Scam keyword count
            is_coord_out        # Coordinate validity flag
        ]
        X.append(feature_vector)
        y.append(0) # Real
        
    # 2. Synthetic Fraud Listings (Realistic Fraud Attack Vectors)
    n_fraud = len(df)
    fraud_types = ['deposit_bait', 'extreme_overprice', 'location_spoof', 'phishing_pressure', 'impossible_specs']
    
    for i in range(n_fraud):
        fraud_type = fraud_types[i % len(fraud_types)]
        source_row = df.iloc[np.random.randint(len(df))]
        
        area = float(source_row['Area'])
        bedrooms = float(source_row['Bedrooms'])
        lat = float(source_row['Latitude'])
        lon = float(source_row['Longitude'])
        
        city_k = str(source_row['City']).lower().strip()
        loc_k = str(source_row['Locality']).lower().strip()
        full_k = f"{city_k}|{loc_k}"
        base_pps = locality_stats.get(full_k, {}).get('median_pps') or overall_pps
        loc_std = locality_stats.get(full_k, {}).get('std_pps', base_pps * 0.2)
        
        pred_fair_log = price_model.predict([[area, bedrooms, lat, lon, base_pps, area * base_pps]])[0]
        fair_price = np.expm1(pred_fair_log)
        
        urgency_kw = 0
        scam_kw = 0
        dist_km = np.random.uniform(0.5, 3.0)
        is_coord_out = 0
        
        if fraud_type == 'deposit_bait':
            # Advance-fee deposit scam: list price is 65% - 92% below fair market value
            discount = np.random.uniform(0.08, 0.35)
            price = fair_price * discount
            urgency_kw = np.random.choice([1, 2, 3])
            scam_kw = np.random.choice([1, 2])
        elif fraud_type == 'extreme_overprice':
            # Absurd overpricing: 3x - 8x fair market value
            multiplier = np.random.uniform(2.8, 6.0)
            price = fair_price * multiplier
        elif fraud_type == 'location_spoof':
            # Coordinates are in wrong district or 15 - 80 km away
            price = fair_price * np.random.uniform(0.7, 1.2)
            dist_km = np.random.uniform(12.0, 65.0)
            is_coord_out = 1
        elif fraud_type == 'phishing_pressure':
            # Heavy scam & wire transfer keywords, unverified urgency
            price = fair_price * np.random.uniform(0.4, 0.7)
            urgency_kw = np.random.choice([2, 3, 4])
            scam_kw = np.random.choice([2, 3, 4])
        else: # impossible_specs
            # 150 sqft with 5 bedrooms, or 10,000 sqft for 20 Lakhs
            if np.random.rand() > 0.5:
                area = np.random.uniform(150, 300)
                bedrooms = 4
                price = 1500000
            else:
                area = np.random.uniform(7000, 12000)
                bedrooms = 1
                price = 2500000
                
        price_ratio = price / max(fair_price, 1000)
        pps = price / area
        pps_zscore = abs(pps - base_pps) / max(loc_std, 100)
        area_per_bed = area / max(bedrooms, 1)
        
        feature_vector = [
            price_ratio,
            pps_zscore,
            dist_km,
            area,
            bedrooms,
            area_per_bed,
            urgency_kw,
            scam_kw,
            is_coord_out
        ]
        X.append(feature_vector)
        y.append(1) # Fake
        
    X = np.array(X)
    y = np.array(y)
    print(f"Generated fraud dataset: {len(X)} samples ({sum(y == 0)} Real, {sum(y == 1)} Fake).")
    return X, y

def train_hybrid_classifier(X, y):
    """
    Train Hybrid ExtraTree + ANN (Multi-Layer Perceptron) Ensemble Classifier
    Saves: hybrid_extra_tree_ann1.pkl, fraud_scaler.pkl
    """
    print("\n--- Training Hybrid ExtraTrees + ANN Fraud Classifier ---")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model A: ExtraTreesClassifier
    et_clf = ExtraTreesClassifier(
        n_estimators=120,
        max_depth=12,
        min_samples_split=4,
        random_state=42
    )
    
    # Model B: Multi-Layer Perceptron (ANN)
    ann_clf = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        max_iter=300,
        random_state=42
    )
    
    # Hybrid Soft Voting Ensemble
    hybrid_model = VotingClassifier(
        estimators=[('extra_trees', et_clf), ('ann', ann_clf)],
        voting='soft',
        weights=[0.6, 0.4]
    )
    
    hybrid_model.fit(X_train_scaled, y_train)
    
    # Evaluation
    preds = hybrid_model.predict(X_test_scaled)
    probs = hybrid_model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)
    
    print("Hybrid Classifier Test Results:")
    print(f"  Accuracy:  {acc * 100:.2f}%")
    print(f"  Precision: {prec * 100:.2f}%")
    print(f"  Recall:    {rec * 100:.2f}%")
    print(f"  F1 Score:  {f1 * 100:.2f}%")
    print(f"  ROC-AUC:   {auc * 100:.2f}%")
    
    # Save hybrid model and scaler
    joblib.dump(hybrid_model, MODELS_DIR / "hybrid_extra_tree_ann1.pkl")
    joblib.dump(scaler, MODELS_DIR / "fraud_scaler.pkl")
    
    feature_names = [
        "price_ratio", "pps_zscore", "dist_km", "area", "bedrooms",
        "area_per_bed", "urgency_kw", "scam_kw", "is_coord_out"
    ]
    with open(MODELS_DIR / "feature_columns.json", "w") as f:
        json.dump(feature_names, f, indent=2)
        
    metrics = {
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "roc_auc": round(auc * 100, 2),
        "model_type": "Hybrid ExtraTree (60%) + ANN MLP (40%)",
        "sample_count": len(X)
    }
    with open(MODELS_DIR / "model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"Saved hybrid model to {MODELS_DIR / 'hybrid_extra_tree_ann1.pkl'}")
    return hybrid_model, metrics

def run_all():
    print("=" * 60)
    print("STARTING MACHINE LEARNING MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    df = load_and_prepare_datasets()
    price_model, loc_stats, city_stats, r2, mape = train_price_predictor(df)
    X, y = generate_fraud_classification_dataset(df, price_model, loc_stats, city_stats)
    hybrid_model, metrics = train_hybrid_classifier(X, y)
    
    print("\n" + "=" * 60)
    print("ALL MODELS TRAINED AND SAVED SUCCESSFULLY!")
    print(f"Fair Price Model R2: {r2:.4f} | MAPE: {mape:.2f}%")
    print(f"Fraud Detection Model Accuracy: {metrics['accuracy']}% | F1: {metrics['f1_score']}%")
    print("=" * 60)

if __name__ == "__main__":
    run_all()

