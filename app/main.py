from fastapi import FastAPI
import logging
import sys
from .api.fraud_routes import router as fraud_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ssp-ai-fraud-detection")

app = FastAPI(title="SSP AI Fraud Detection")

app.include_router(fraud_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "SSP AI Fraud Detection is running"}
