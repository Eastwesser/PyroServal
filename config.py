import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DB_URL = os.getenv('DB_URL')

    print(f"Loaded DB_URL: {DB_URL}")  # Add this line to debug
