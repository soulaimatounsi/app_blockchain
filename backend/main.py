from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import hashlib

from ml_inference import analyze_contract

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_SCORES = {
    "XGBoost": {"precision": 0.92, "recall": 0.90, "f1": 0.91}
}

def infer_vulnerabilities(features):
    vulns = []

    if features["num_calls"] > 0:
        vulns.append("Reentrancy risk")

    if features["num_delegatecall"] > 0:
        vulns.append("Dangerous delegatecall usage")

    if features["num_selfdestruct"] > 0:
        vulns.append("Selfdestruct detected")

    if features["uses_safemath"] == 0:
        vulns.append("Possible integer overflow")

    if not vulns:
        vulns.append("No critical vulnerability detected")

    return vulns

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    code = (await file.read()).decode("utf-8", errors="ignore")

    features, predictions = analyze_contract(code)

    model_used = "XGBoost"
    verdict = "Vulnerable" if predictions["XGBoost"] == 1 else "Safe"

    audit_hash = hashlib.sha256(code.encode()).hexdigest()

    return {
        "sourceCode": code,
        "modelUsed": model_used,
        "prediction": verdict,
        "detectedVulnerabilities": infer_vulnerabilities(features),
        "score": MODEL_SCORES[model_used],
        "blockchainTrace": {
            "hash": audit_hash,
            "txLink": "pending"
        }
    }
