"""
Configuration module for Sahayyak Voice Assistant.
Loads environment variables and provides typed configuration.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class BhashiniConfig:
    """Bhashini API configuration."""

    user_id: str
    ulca_api_key: str
    inference_key: str
    pipeline_id: str = "64392f96daac500b55c543cd"

    @classmethod
    def from_env(cls) -> "BhashiniConfig":
        return cls(
            user_id=os.getenv("BHASHINI_USER_ID", ""),
            ulca_api_key=os.getenv("BHASHINI_ULCA_API_KEY", ""),
            inference_key=os.getenv("BHASHINI_INFERENCE_KEY", ""),
        )

    def is_configured(self) -> bool:
        return all([self.user_id, self.ulca_api_key, self.inference_key])


@dataclass
class GeminiConfig:
    """Google Gemini configuration."""

    api_key: str
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_tokens: int = 1024

    @classmethod
    def from_env(cls) -> "GeminiConfig":
        return cls(
            api_key=os.getenv("GOOGLE_API_KEY", ""),
        )

    def is_configured(self) -> bool:
        return bool(self.api_key)


@dataclass
class LangSmithConfig:
    """LangSmith observability configuration."""

    api_key: str
    project: str
    tracing_enabled: bool

    @classmethod
    def from_env(cls) -> "LangSmithConfig":
        return cls(
            api_key=os.getenv("LANGCHAIN_API_KEY", ""),
            project=os.getenv("LANGCHAIN_PROJECT", "sahayyak"),
            tracing_enabled=os.getenv("LANGCHAIN_TRACING_V2", "false").lower()
            == "true",
        )


@dataclass
class AppConfig:
    """Main application configuration."""

    environment: str
    log_level: str
    data_dir: Path
    vectordb_dir: Path

    @classmethod
    def from_env(cls) -> "AppConfig":
        base_dir = Path(__file__).parent.parent
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            data_dir=base_dir / "data",
            vectordb_dir=base_dir / "data" / "vectordb",
        )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@dataclass
class Config:
    """Root configuration container."""

    app: AppConfig
    bhashini: BhashiniConfig
    gemini: GeminiConfig
    langsmith: LangSmithConfig

    @classmethod
    def load(cls) -> "Config":
        """Load all configuration from environment."""
        return cls(
            app=AppConfig.from_env(),
            bhashini=BhashiniConfig.from_env(),
            gemini=GeminiConfig.from_env(),
            langsmith=LangSmithConfig.from_env(),
        )


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config
