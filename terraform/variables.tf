variable "aws_region" { type = string; default = "us-east-1" }
variable "environment" { type = string }
variable "container_image" { type = string; default = "placeholder" }

variable "bedrock_model_id_param_name" {
  type        = string
  description = "The name of the SSM parameter for the Bedrock model ID."
  default     = "ssp/ai/fraud_model_id"
}
