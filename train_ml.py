import os
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

def train_and_save_ml_models():
    base_dir = "/Users/tanmaykalra/jaundice_detection"
    csv_path = os.path.join(base_dir, "raw_data", "NJN", "code_data", "Pythons_Code_AI_Testing_Data", "Excel File", "train.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # In NJN train.csv: class 1 = normal, class 2 = jaundice (or vice versa in labels)
    # Let's inspect class distribution
    print("Class counts:\n", df['class'].value_counts())
    
    feature_cols = ['red', 'green', 'blue', 'Y', 'cblue', 'cred']
    X = df[feature_cols].copy()
    y = df['class'].values
    
    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # Adjust classes if needed for XGBoost (0-indexed: map min class to 0)
    min_label = y.min()
    y_train_xgb = y_train - min_label
    y_test_xgb = y_test - min_label
    
    print("Training XGBoost Classifier...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    xgb_model.fit(X_train, y_train_xgb)
    
    preds_xgb = xgb_model.predict(X_test) + min_label
    acc_xgb = accuracy_score(y_test, preds_xgb)
    print(f"XGBoost Test Accuracy: {acc_xgb * 100:.2f}%")
    print(classification_report(y_test, preds_xgb))
    
    # Random Forest
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    preds_rf = rf_model.predict(X_test)
    acc_rf = accuracy_score(y_test, preds_rf)
    print(f"Random Forest Test Accuracy: {acc_rf * 100:.2f}%")
    
    # Save artifacts
    artifacts = {
        'xgb_model': xgb_model,
        'rf_model': rf_model,
        'scaler': scaler,
        'feature_cols': feature_cols,
        'min_label': min_label,
        'label_mapping': {1: 'Normal', 2: 'Jaundice'}
    }
    
    save_path = os.path.join(models_dir, "tabular_models.joblib")
    joblib.dump(artifacts, save_path)
    print(f"Saved tabular models to {save_path}")

if __name__ == "__main__":
    train_and_save_ml_models()
