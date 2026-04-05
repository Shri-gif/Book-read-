from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    openai_key: str
    templates_dir: str = "static/templates"
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    
    class Config:
        env_file = "config.yaml"

settings = Settings() 
