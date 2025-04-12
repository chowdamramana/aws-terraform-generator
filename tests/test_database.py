import pytest
from app.services.database import save_config, get_user_configs
from app.models.config import AWSConfig, ResourceConfig

def test_save_and_get_config():
    config = AWSConfig(
        region="us-east-1",
        resources=[
            ResourceConfig(
                resource_type="aws_instance",
                properties={"ami": "ami-12345678", "instance_type": "t2.micro"}
            )
        ]
    )
    config_id = save_config(config, user_id=1)
    assert config_id > 0

    configs = get_user_configs(user_id=1)
    assert len(configs) >= 1
    assert configs[0].region == "us-east-1"