from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel

class LLMApiKeys(BaseModel):
    mistral: str
    openai: str

class NotionConfig(BaseModel):
    api_key: str
    database_id: str

class TelegramConfig(BaseModel):
    bot_token: str

class ModelNames(BaseModel):
    embedding: str = "mistral-embed"
    reasoner: str
    tool_caller: str
    writer: str

class SearchConfig(BaseModel):
    similarity_threshold: float = 0.7
    max_results: int = 1
    sync_batch_size: int = 100

class DatabaseConfig(BaseModel):
    url: str

class Settings(BaseModel):
    llm_api_keys: LLMApiKeys
    notion: NotionConfig
    telegram: TelegramConfig
    model_names: ModelNames
    search: SearchConfig
    database: DatabaseConfig

def load_config() -> Settings:
    """Load configuration from YAML file with environment variable interpolation."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    # Load YAML with environment variable interpolation
    import os
    from string import Template

    with open(config_path) as f:
        template = Template(f.read())
        config_str = template.substitute(os.environ)
        config_dict = yaml.safe_load(config_str)

    return Settings(**config_dict)

settings = load_config() 