# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEFAULT_PROVIDER = "groq"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 3

APP_NAME = "TalkDB"
APP_VERSION = "0.1.0"