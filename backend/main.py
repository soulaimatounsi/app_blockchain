from fastapi import FastAPI, UploadFile
import joblib
import numpy as np
from utils.parser import extract_features
from llm_tester import LLMSecurityTester
from connect import store_record  # <-- nouvel import
import os

app = FastAPI()

# Charger les modèles existants
logistic = joblib.load("models/logistic.pkl")
rf = joblib.load("models/random_forest.pkl")
xgb = joblib.load("models/xgboost.pkl")

llm_tester = LLMSecurityTester(os.getenv("MISTRAL_API_KEY"))

@app.post("/analyze")
async def analyze_contract(file: UploadFile):
    code = (await file.read()).decode("utf-8")

    # 1️⃣ Feature extraction
    features_dict = extract_features(code)
    X = np.array([list(features_dict.values())])

    # 2️⃣ ML predictions
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

    best_model = max(results.items(), key=lambda x: x[1]["score"])

    # 3️⃣ LLM result
    llm_result = llm_tester.analyze_contract(code)

    # 4️⃣ Blockchain: store ML and LLM hashes
    ml_record = store_record(
        contract_identifier="ContractXYZ",
        result_type="ML",
        record_data=results,
        model_name=best_model[0]
    )

    llm_record = store_record(
        contract_identifier="ContractXYZ",
        result_type="LLM",
        record_data=llm_result,
        model_name=llm_result.get("model_name", "MISTRAL")
    )

    return {
        "contract_code": code,
        "all_results": results,
        "best_model": best_model[0],
        "best_score": best_model[1]["score"],
        "llm_result": llm_result,
        "blockchain_ml": ml_record,
        "blockchain_llm": llm_record
    }
