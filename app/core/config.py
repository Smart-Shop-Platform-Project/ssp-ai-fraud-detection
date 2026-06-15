from pydantic_settings import BaseSettings
import os
import boto3
import logging

logger = logging.getLogger("ssp-ai-fraud-detection")

def get_ssm_parameter(name, region):
    try:
        ssm_client = boto3.client('ssm', region_name=region)
        parameter = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return parameter['Parameter']['Value']
    except Exception as e:
        logger.critical(f"Error fetching parameter {name}: {e}")
        raise

class Settings(BaseSettings):
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID_PARAM_NAME: str = os.environ.get("BEDROCK_MODEL_ID_PARAM_NAME", "/ssp/ai/fraud_model_id")
    BEDROCK_MODEL_ID: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.BEDROCK_MODEL_ID = get_ssm_parameter(self.BEDROCK_MODEL_ID_PARAM_NAME, self.AWS_REGION)
        except Exception:
             self.BEDROCK_MODEL_ID = "anthropic.claude-v2"

settings = Settings()
