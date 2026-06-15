import boto3
from ..core.config import settings
import logging
import json

logger = logging.getLogger("ssp-ai-fraud-detection")

class FraudDetectionService:
    def __init__(self):
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)

    async def detect_fraud(self, transaction_data: dict):
        if not settings.BEDROCK_MODEL_ID:
            logger.error("Bedrock model ID is not configured")
            raise Exception("Bedrock model ID not configured")
            
        try:
            logger.info(f"Invoking Bedrock model {settings.BEDROCK_MODEL_ID} for fraud detection")
            prompt = f"Analyze the following transaction for fraud and respond with only 'true' or 'false': {json.dumps(transaction_data)}"
            
            body = json.dumps({
                "prompt": f"\n\nHuman:{prompt}\n\nAssistant:",
                "max_tokens_to_sample": 10,
                "temperature": 0.1,
            })
            
            response = self.bedrock_runtime.invoke_model(
                body=body, 
                modelId=settings.BEDROCK_MODEL_ID, 
                accept='application/json', 
                contentType='application/json'
            )
            
            result = json.loads(response.get('body').read())
            is_fraud = "true" in result.get('completion', '').lower()
            
            return {"is_fraud": is_fraud}
        except Exception as e:
            logger.error(f"Failed to detect fraud: {e}")
            raise
