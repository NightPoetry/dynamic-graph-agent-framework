from dataclasses import dataclass, field
from typing import Optional
import yaml
import os

@dataclass
class AIConfig:
    api_key: str
    base_url: str
    model: str = "qwen-plus"
    temperature: float = 0.1
    streaming: bool = True
    max_retries: int = 3
    timeout: int = 60
    
    @classmethod
    def from_yaml(cls, config_path: str) -> 'AIConfig':
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'AIConfig':
        return cls(**config_dict)
