terraform {
  backend "s3" {
    bucket         = "classic-library-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "classic-library-terraform-locks"
    encrypt        = true
  }
}
