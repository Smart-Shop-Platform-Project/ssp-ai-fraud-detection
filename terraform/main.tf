terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {}
}

provider "aws" { region = var.aws_region }

data "aws_caller_identity" "current" {}

# IAM Policy for SSM and Bedrock Access
resource "aws_iam_policy" "fraud_policy" {
  name        = "ssp-ai-fraud-detection-policy-${var.environment}"
  description = "Allows reading SSM params and invoking Bedrock"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "ssm:GetParameter",
        Effect   = "Allow",
        Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.bedrock_model_id_param_name}"
      },
      {
        Action   = "bedrock:InvokeModel",
        Effect   = "Allow",
        Resource = "*" // Should be restricted to the specific model ARN in a real scenario
      }
    ]
  })
}

module "ecr" {
  source          = "git::https://github.com/DeathGod049/terraform-infra-child.git//modules/ecr?ref=v0.1.0"
  repository_name = "ssp-ai-fraud-detection"
  environment     = var.environment
}

module "lambda_service" {
  source              = "git::https://github.com/DeathGod049/terraform-infra-child.git//modules/lambda-service?ref=v0.1.0"
  function_name       = "ssp-ai-fraud-detection"
  environment         = var.environment
  container_image     = var.container_image

  execution_policy_arns = [aws_iam_policy.fraud_policy.arn]

  environment_variables = {
    BEDROCK_MODEL_ID_PARAM_NAME = var.bedrock_model_id_param_name
    AWS_REGION                  = var.aws_region
  }
}
