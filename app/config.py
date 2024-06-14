import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
DB_URL = os.getenv("DB_URL")
ENGINE_URL = os.getenv("ENGINE_URL")
SESSION_NAME = os.getenv("SESSION_NAME")
