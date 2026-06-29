from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # LLM Provider (Groq)
    groq_api_key: Optional[str] = None

    # Model Settings
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024
    top_k_recommendations: int = 5

    # Data
    dataset_cache_dir: str = "./data/cache"
    huggingface_dataset: str = "ManikaSaini/zomato-restaurant-recommendation"

    # App
    app_port: int = 8501
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_cache_dir(self) -> Path:
        """Returns the cache directory as a Path object, creating it if it doesn't exist."""
        path = Path(self.dataset_cache_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global settings instance
settings = Settings()
