terraform {
  backend "s3" {
    bucket         = "devops-s3-terraform-state-suman"
    key            = "task1/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}
