import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Config:
    """Application configuration"""

    # Jev Configuration
    JEV_API_ENDPOINT = os.getenv("JEV_API_ENDPOINT", "http://localhost:8000/api/v1/jev")
    JEV_API_KEY = os.getenv("JEV_API_KEY", "mock-api-key")
    JEV_TIMEOUT = 30  # seconds

    # Application Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Request Configuration
    MAX_MESSAGE_LENGTH = 5000
    MIN_MESSAGE_LENGTH = 10

    @classmethod
    def is_development(cls) -> bool:
        return cls.ENVIRONMENT == "development"

    @classmethod
    def is_production(cls) -> bool:
        return cls.ENVIRONMENT == "production"
