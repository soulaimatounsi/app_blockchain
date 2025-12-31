from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
import joblib
import hashlib
import numpy as np
from utils.parser import extract_features

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Charger les modèles EXISTANTS
logistic = joblib.load("models/logistic.pkl")
rf = joblib.load("models/random_forest.pkl")
xgb = joblib.load("models/xgboost.pkl")


@app.post("/analyze")
async def analyze_contract(file: UploadFile):
    code = (await file.read()).decode("utf-8")

    # 1. Feature extraction
    features_dict = extract_features(code)
    X = np.array([list(features_dict.values())])

    # 2. Prédictions de TOUS les modèles
    results = {
        "Logistic Regression": {
            "prediction": int(logistic.predict(X)[0]),
            "score": float(logistic.predict_proba(X)[0][1])
        },
        "Random Forest": {
            "prediction": int(rf.predict(X)[0]),
            "score": float(rf.predict_proba(X)[0][1])
        },
        "XGBoost": {
            "prediction": int(xgb.predict(X)[0]),
            "score": float(xgb.predict_proba(X)[0][1])
        }
    }

    # 3. Sélection du meilleur modèle
    best_model = max(results.items(), key=lambda x: x[1]["score"])

    # 4. Hash blockchain (phase 4 simulée)
    report_hash = hashlib.sha256(
        str(results).encode()
    ).hexdigest()

    return {
        "contract_code": code,
        "all_results": results,
        "best_model": best_model[0],
        "best_score": best_model[1]["score"],
        "blockchain_link": f"https://etherscan.io/tx/{report_hash}"
    }
