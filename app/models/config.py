from pydantic import BaseModel, field_validator, FieldValidationInfo
from typing import Dict, List, Optional
import re
import bleach

class ResourceConfig(BaseModel):
    resource_type: str
    properties: Dict[str, str]

    @field_validator("resource_type")
    def validate_resource_type(cls, value: str) -> str:
        from app.services.resource_metadata import get_resource_types_sync
        resource_types = get_resource_types_sync()
        if value not in resource_types:
            raise ValueError(f"Invalid resource type: {value}")
        return value

    @field_validator("properties")
    def validate_properties(cls, value: Dict[str, str], info: FieldValidationInfo) -> Dict[str, str]:
        from app.services.resource_metadata import get_resource_properties
        resource_type = info.data.get("resource_type")
        if not resource_type:
            return value

        sanitized = {k: bleach.clean(v) for k, v in value.items()}
        properties_metadata = get_resource_properties(resource_type)
        required_fields = [p["name"] for p in properties_metadata if p.get("required")]

        for field in required_fields:
            if field not in sanitized or not sanitized[field]:
                raise ValueError(f"{field} is required for {resource_type}")

        if resource_type == "aws_vpc" and "cidr_block" in sanitized:
            cidr = sanitized["cidr_block"]
            if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$", cidr):
                raise ValueError("Invalid CIDR block format")
        elif resource_type == "aws_s3_bucket" and "bucket" in sanitized:
            bucket = sanitized["bucket"]
            if not re.match(r"^[a-z0-9.-]{3,63}$", bucket):
                raise ValueError("Invalid S3 bucket name")

        return sanitized

class AWSConfig(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    name: Optional[str] = "My Configuration"
    region: str
    resources: List[ResourceConfig]
    version: Optional[int] = 1

    @field_validator("region")
    def validate_region(cls, value: str) -> str:
        valid_regions = [
            "us-east-1", "us-west-2", "eu-west-1", "ap-south-1",
        ]
        if value not in valid_regions:
            raise ValueError("Invalid AWS region")
        return value

    class Config:
        from_attributes = True