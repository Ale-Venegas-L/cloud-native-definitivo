data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/lambda/pre_token_generation.py"
  output_path = "${path.module}/lambda/pre_token_generation.zip"
}

resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-pre-token-lambda"

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
  name = "${var.project_name}-cognito-read"
  role = aws_iam_role.lambda.id

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
  function_name = "${var.project_name}-pre-token-generation"
  role          = aws_iam_role.lambda.arn
  handler       = "pre_token_generation.lambda_handler"
  runtime       = "python3.12"
  timeout       = 10

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  tags = {
    Name = "${var.project_name}-pre-token-lambda"
  }
}

resource "aws_lambda_permission" "cognito" {
  statement_id  = "AllowCognitoInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pre_token_generation.function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.main.arn
}
