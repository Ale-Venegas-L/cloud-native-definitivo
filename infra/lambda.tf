data "archive_file" "lambda" {
  count         = var.enable_cognito ? 1 : 0
  type          = "zip"
  source_file   = "${path.module}/lambda/pre_token_generation.py"
  output_path   = "${path.module}/lambda/pre_token_generation.zip"
}

resource "aws_iam_role" "lambda" {
  count = var.enable_cognito ? 1 : 0
  name  = "${var.project_name}-pre-token-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Name = "${var.project_name}-lambda-role"
  }
}

resource "aws_iam_role_policy" "lambda_cognito" {
  count = var.enable_cognito ? 1 : 0
  name  = "${var.project_name}-cognito-read"
  role  = aws_iam_role.lambda[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["cognito-idp:AdminGetUser"]
      Resource = "*"
    }]
  })
}

resource "aws_lambda_function" "pre_token_generation" {
  count         = var.enable_cognito ? 1 : 0
  function_name = "${var.project_name}-pre-token-generation"
  role          = aws_iam_role.lambda[0].arn
  handler       = "pre_token_generation.lambda_handler"
  runtime       = "python3.12"
  timeout       = 10

  filename         = data.archive_file.lambda[0].output_path
  source_code_hash = data.archive_file.lambda[0].output_base64sha256

  tags = {
    Name = "${var.project_name}-pre-token-lambda"
  }
}

resource "aws_lambda_permission" "cognito" {
  count         = var.enable_cognito ? 1 : 0
  statement_id  = "AllowCognitoInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pre_token_generation[0].function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.main[0].arn
}
