import pytest
from unittest.mock import patch, AsyncMock
from app.services.fraud_service import FraudDetectionService

def test_detect_fraud_api_is_fraud(client):
    with patch.object(FraudDetectionService, 'detect_fraud', new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = {"is_fraud": True}
        
        request_body = {
            "amount": 5000,
            "location": "unknown"
        }
        
        response = client.post("/api/v1/detect-fraud", json=request_body)
        
        assert response.status_code == 200
        assert response.json() == {"is_fraud": True}
        mock_detect.assert_called_once_with(request_body)

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SSP AI Fraud Detection is running"}
