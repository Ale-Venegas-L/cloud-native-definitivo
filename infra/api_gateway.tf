resource "aws_api_gateway_rest_api" "main" {
  name = "${var.project_name}-api"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "${var.project_name}-api"
  }
}

resource "aws_api_gateway_resource" "api" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "api"
}

resource "aws_api_gateway_resource" "v1" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api.id
  path_part   = "v1"
}

resource "aws_api_gateway_resource" "books" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "books"
}

resource "aws_api_gateway_resource" "books_id" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.books.id
  path_part   = "{id}"
}

resource "aws_api_gateway_resource" "authors" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "authors"
}

resource "aws_api_gateway_resource" "authors_id" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.authors.id
  path_part   = "{id}"
}

resource "aws_api_gateway_resource" "authors_id_books" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.authors_id.id
  path_part   = "books"
}

resource "aws_api_gateway_resource" "auth" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "auth"
}

resource "aws_api_gateway_resource" "auth_me" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.auth.id
  path_part   = "me"
}

resource "aws_api_gateway_resource" "health" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "health"
}

resource "aws_api_gateway_authorizer" "cognito" {
  count         = var.enable_cognito ? 1 : 0
  name          = "${var.project_name}-cognito-authorizer"
  rest_api_id   = aws_api_gateway_rest_api.main.id
  type          = "COGNITO_USER_POOLS"
  provider_arns = [aws_cognito_user_pool.main[0].arn]
}

locals {
  api_methods = {
    books_any = {
      resource_id   = aws_api_gateway_resource.books.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1/books"
    }
    books_id_any = {
      resource_id   = aws_api_gateway_resource.books_id.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1/books/{id}"
    }
    authors_any = {
      resource_id   = aws_api_gateway_resource.authors.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1/authors"
    }
    authors_id_any = {
      resource_id   = aws_api_gateway_resource.authors_id.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1/authors/{id}"
    }
    authors_id_books_any = {
      resource_id   = aws_api_gateway_resource.authors_id_books.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1/authors/{id}/books"
    }
    auth_me_get = {
      resource_id   = aws_api_gateway_resource.auth_me.id
      http_method   = "GET"
      authorization = var.enable_cognito ? "COGNITO_USER_POOLS" : "NONE"
      authorizer_id = var.enable_cognito ? aws_api_gateway_authorizer.cognito[0].id : null
      backend_path  = "/api/v1/auth/me"
    }
    health_get = {
      resource_id   = aws_api_gateway_resource.health.id
      http_method   = "GET"
      authorization = "NONE"
      backend_path  = "/api/v1/health"
    }
    v1_any = {
      resource_id   = aws_api_gateway_resource.v1.id
      http_method   = "ANY"
      authorization = "NONE"
      backend_path  = "/api/v1"
    }
  }
}

resource "aws_api_gateway_method" "methods" {
  for_each = local.api_methods

  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = each.value.resource_id
  http_method   = each.value.http_method
  authorization = each.value.authorization
  authorizer_id = try(each.value.authorizer_id, null)
}

resource "aws_api_gateway_integration" "integrations" {
  for_each = local.api_methods

  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = each.value.resource_id
  http_method             = aws_api_gateway_method.methods[each.key].http_method
  integration_http_method = "ANY"
  type                    = "HTTP"
  uri                     = "http://${aws_instance.app.public_ip}:8000${each.value.backend_path}"
}

locals {
  cors_resources = {
    "v1"               = aws_api_gateway_resource.v1.id
    "books"            = aws_api_gateway_resource.books.id
    "books_id"         = aws_api_gateway_resource.books_id.id
    "authors"          = aws_api_gateway_resource.authors.id
    "authors_id"       = aws_api_gateway_resource.authors_id.id
    "authors_id_books" = aws_api_gateway_resource.authors_id_books.id
    "auth_me"          = aws_api_gateway_resource.auth_me.id
    "health"           = aws_api_gateway_resource.health.id
  }
}

resource "aws_api_gateway_method" "options" {
  for_each = local.cors_resources

  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = each.value
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = each.value
  http_method = "OPTIONS"
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }

  depends_on = [aws_api_gateway_method.options]
}

resource "aws_api_gateway_method_response" "options_200" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = each.value
  http_method = "OPTIONS"
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  response_models = {
    "application/json" = "Empty"
  }

  depends_on = [aws_api_gateway_integration.options]
}

resource "aws_api_gateway_integration_response" "options_200" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = each.value
  http_method = "OPTIONS"
  status_code = aws_api_gateway_method_response.options_200[each.key].status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,PUT,DELETE,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  depends_on = [
    aws_api_gateway_integration.integrations,
    aws_api_gateway_integration.options,
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "prod"
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "dev"
}
