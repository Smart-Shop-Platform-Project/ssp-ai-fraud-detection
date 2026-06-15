# SSP AI Fraud Detection Service

This service performs real-time fraud analysis on transactions using Large Language Models via Amazon Bedrock. It is built using FastAPI and deployed as an AWS Lambda function using Mangum.

## Architecture
- **Framework:** FastAPI
- **Deployment:** AWS Lambda (Container Image)
- **Integration:** Amazon Bedrock Runtime (e.g., Anthropic Claude)
- **Secrets:** AWS Systems Manager (SSM) Parameter Store

## Prerequisites
- Python 3.12
- Access to Amazon Bedrock models in your AWS account.
- The Bedrock Model ID must be stored in AWS SSM Parameter Store.

## Local Development
1. Create a virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` and `pip install -r requirements-dev.txt`
4. Set the `AWS_REGION` environment variable. Ensure your AWS credentials have permission to invoke the Bedrock model.
5. Run the application: `uvicorn app.main:app --reload`
