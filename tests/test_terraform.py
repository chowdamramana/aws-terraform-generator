import pytest
from app.services.terraform import generate_terraform_files
from app.models.config import AWSConfig, ResourceConfig

def test_generate_terraform():
    config = AWSConfig(
        region="us-east-1",
        resources=[
            ResourceConfig(
                resource_type="aws_instance",
                properties={"ami": "ami-12345678", "instance_type": "t2.micro"}
            )
        ]
    )
    files = generate_terraform_files(config)
    assert "main.tf" in files
    assert "provider \"aws\"" in files["main.tf"]
    assert "variables.tf" in files
    assert "outputs.tf" in files