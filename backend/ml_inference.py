import joblib
from utils.parser import extract_features

lr = joblib.load("models/logistic.pkl")
rf = joblib.load("models/random_forest.pkl")
xgb = joblib.load("models/xgboost.pkl")

def analyze_contract(code):
    features = extract_features(code)
    X = [list(features.values())]

    predictions = {
        "LogisticRegression": int(lr.predict(X)[0]),
        "RandomForest": int(rf.predict(X)[0]),
        "XGBoost": int(xgb.predict(X)[0]),
    }

    return features, predictions