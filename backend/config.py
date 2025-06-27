import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug: Print the environment variables (useful for debugging)
print(f"DEBUG: Loading GEMINI_API_KEY from environment: {os.getenv('GEMINI_API_KEY')}")
print(f"DEBUG: Loading MONGO_URI from environment: {os.getenv('MONGO_URI')}")

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/healthcoach")  # Default MongoDB URI
    DB_NAME = os.getenv("DB_NAME", "healthcoachdb")  # Default database name
    SECRET_KEY = os.getenv("SECRET_KEY", "x8YqxBo7YstPlKIcDkM_Oee3Y4y3drE5")  # Default secret key if not set
    GEMINI_API_KEY = os.getenv("AIzaSyAPICBe_CZLuJLmxz5Hc6DFBijtMiFIQiQ")  # Ensure GEMINI_API_KEY is loaded from environment
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")  # True if DEBUG is "true", "1", or "t"
