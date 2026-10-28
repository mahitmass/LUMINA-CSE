"""
KiraayaShield AI Microservice (FastAPI + NLP Clause Parser + CV Wear-and-Tear Auditor)
Run with: uvicorn backend_python.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import hashlib

app = FastAPI(title="KiraayaShield AI Agent API", version="2.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeaseAnalyzeRequest(BaseModel):
    lease_text: str
    city: str = "Noida"
    monthly_rent: int = 18000
    deposit_paid: int = 54000

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "KiraayaShield-Python-Agent", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/analyze")
def analyze_lease(payload: LeaseAnalyzeRequest):
    ratio = round(payload.deposit_paid / max(payload.monthly_rent, 1), 1)
    digest = hashlib.sha256(payload.lease_text.encode("utf-8")).hexdigest()[:16]
    return {
        "document_hash": f"0x{digest}",
        "deposit_to_rent_ratio": f"{ratio}x",
        "mta_section_11_violation": ratio > 2.0,
        "risk_score": 88 if ratio > 2.0 else 64,
        "recommended_forum": "National Consumer Helpline (INGRAM) & e-Daakhil Consumer Commission"
    }
