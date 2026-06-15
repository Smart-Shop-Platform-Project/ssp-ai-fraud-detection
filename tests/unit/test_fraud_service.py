import pytest
import json
from unittest.mock import patch, MagicMock
from app.services.fraud_service import FraudDetectionService

# A dummy implementation of the settings to isolate tests from SSM
class DummySettings:
    AWS_REGION = "us-east-1"
    BEDROCK_MODEL_ID = "test-model-id"

@pytest.fixture
def mock_bedrock_runtime():
    # We patch boto3.client where it is called inside the service class
    with patch("boto3.client") as mock_client:
        mock_runtime = MagicMock()
        mock_client.return_value = mock_runtime
        yield mock_runtime

@pytest.fixture
def fraud_service(mock_bedrock_runtime):
    with patch("app.services.fraud_service.settings", DummySettings()):
        # Initialize the service. Because of the fixture above, 
        # it will use the mocked boto3 client.
        return FraudDetectionService()

@pytest.mark.asyncio
async def test_detect_fraud_is_fraud(fraud_service, mock_bedrock_runtime):
    # Setup the mock response from Bedrock to simulate a fraudulent transaction
    mock_response_body = MagicMock()
    mock_response_body.read.return_value = json.dumps({"completion": "The transaction seems suspicious. True."}).encode('utf-8')
    mock_bedrock_runtime.invoke_model.return_value = {"body": mock_response_body}

    transaction_data = {"amount": 5000, "location": "unknown"}

    # Execute
    result = await fraud_service.detect_fraud(transaction_data)

    # Assert
    assert result == {"is_fraud": True}
    # Verify the model was invoked with the right model ID from dummy settings
    mock_bedrock_runtime.invoke_model.assert_called_once()
    call_args = mock_bedrock_runtime.invoke_model.call_args[1]
    assert call_args["modelId"] == "test-model-id"

@pytest.mark.asyncio
async def test_detect_fraud_is_not_fraud(fraud_service, mock_bedrock_runtime):
    # Setup the mock response from Bedrock to simulate a clean transaction
    mock_response_body = MagicMock()
    mock_response_body.read.return_value = json.dumps({"completion": "Looks normal. False."}).encode('utf-8')
    mock_bedrock_runtime.invoke_model.return_value = {"body": mock_response_body}

    transaction_data = {"amount": 50, "location": "home"}

    # Execute
    result = await fraud_service.detect_fraud(transaction_data)

    # Assert
    assert result == {"is_fraud": False}

@pytest.mark.asyncio
async def test_detect_fraud_missing_model_id(fraud_service):
    # Setup: override the dummy settings to simulate missing configuration
    with patch("app.services.fraud_service.settings.BEDROCK_MODEL_ID", None):
        with pytest.raises(Exception) as exc_info:
            await fraud_service.detect_fraud({"amount": 10})
        
        assert str(exc_info.value) == "Bedrock model ID not configured"
