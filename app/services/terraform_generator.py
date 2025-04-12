from typing import List
from app.models.config import AWSConfig, TerraformOutput
import structlog

logger = structlog.get_logger(__name__)

def generate_terraform_code(config: AWSConfig) -> TerraformOutput:
    """
    Generate Terraform .tf file content from AWSConfig.
    """
    try:
        tf_lines = [
            'provider "aws" {',
            f'  region = "{config.region}"',
            '}',
            '',
        ]

        for resource in config.resources:
            resource_type = resource.resource_type
            resource_name = f"{resource_type}_{config.id or 'default'}"
            tf_lines.append(f'resource "{resource_type}" "{resource_name}" {{')
            
            for key, value in resource.properties.items():
                # Handle boolean and list types appropriately
                if value.lower() in ("true", "false"):
                    tf_lines.append(f'  {key} = {value.lower()}')
                elif value.startswith("[") and value.endswith("]"):
                    tf_lines.append(f'  {key} = {value}')
                else:
                    tf_lines.append(f'  {key} = "{value}"')
            
            tf_lines.append('}')
            tf_lines.append('')

        content = "\n".join(tf_lines)
        logger.info("Generated Terraform code", config_id=config.id)
        return TerraformOutput(content=content)
    except Exception as e:
        logger.error("Failed to generate Terraform code", error=str(e))
        raise