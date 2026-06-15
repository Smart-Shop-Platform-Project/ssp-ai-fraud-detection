from fastapi import APIRouter, HTTPException
from ..services.fraud_service import FraudDetectionService

router = APIRouter()
fraud_service = FraudDetectionService()

@router.post("/detect-fraud", tags=["Fraud Detection"])
async def detect_fraud(transaction_data: dict):
    try:
        return await fraud_service.detect_fraud(transaction_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
