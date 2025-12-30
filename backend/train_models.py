import os
import re
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from utils.parser import extract_features

# ======================
# DATASET LOADING
# ======================
def load_dataset(safe_csv, vuln_csv):
    safe_df = pd.read_csv(safe_csv)
    vuln_df = pd.read_csv(vuln_csv)
    
    # Sécurité : suppression des lignes vides
    safe_df = safe_df.dropna(subset=["code"])
    vuln_df = vuln_df.dropna(subset=["code"])

    safe_features = pd.DataFrame(
        [extract_features(code) for code in safe_df["code"]]
    )
    safe_features["label"] = 0

    vuln_features = pd.DataFrame(
        [extract_features(code) for code in vuln_df["code"]]
    )
    vuln_features["label"] = 1

    dataset = pd.concat([safe_features, vuln_features], ignore_index=True)
    return dataset

# ======================
# TRAINING FUNCTIONS
# ======================
def train_logistic_regression(dataset):
    X = dataset.drop("label", axis=1)
    y = dataset["label"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    return model

def train_random_forest(dataset):
    X = dataset.drop("label", axis=1)
    y = dataset["label"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_xgboost(dataset):
    X = dataset.drop("label", axis=1)
    y = dataset["label"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    return model

# ======================
# MAIN
# ======================
if __name__ == "__main__":

    SAFE_CSV = "data/Safe_Contract.csv"
    VULN_CSV = "data/Vulnerable_Contract.csv"

    print("📥 Loading dataset...")
    dataset = load_dataset(SAFE_CSV, VULN_CSV)

    print("🤖 Training models...")
    lr = train_logistic_regression(dataset)
    rf = train_random_forest(dataset)
    xgb = train_xgboost(dataset)

    os.makedirs("models", exist_ok=True)

    joblib.dump(lr, "models/logistic.pkl")
    joblib.dump(rf, "models/random_forest.pkl")
    joblib.dump(xgb, "models/xgboost.pkl")

    print("✅ Models trained and saved successfully")
