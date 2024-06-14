import logging

from pyrogram import Client

from .config import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "pyro_serval",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_NAME,
)
