from os import getenv as gtnv
from pathlib import Path

from loguru import logger

from dotenv import load_dotenv
load_dotenv()


DEBUG: bool = gtnv("DEBUG") == "1"

BASE_DIR = Path(__file__).parent


logger.add(
    BASE_DIR / "logs/debug_logs.log" if DEBUG else BASE_DIR / "logs/bot.log",
    rotation="00:00:00",
    level="DEBUG" if DEBUG else "INFO",
)

postgres_settings: dict = {
    "username": gtnv("POSTGRES_USER") or "admin",
    "password": gtnv("POSTGRES_PASSWORD") or "admin",
    "host": gtnv("POSTGRES_HOST") or "localhost",
    "port": gtnv("POSTGRES_PORT") or 5432,
    "db_name": gtnv("POSTGRES_DB") or "admin",
}

DB_URL: str = (
    f"postgresql+asyncpg://"
    f"{postgres_settings.get('username')}:"
    f"{postgres_settings.get('password')}@"
    f"{postgres_settings.get('host')}:"
    f"{postgres_settings.get('port')}/"
    f"{postgres_settings.get('db_name')}"
)

API_ID: str = gtnv("API_ID")

if not API_ID:
    raise ValueError("No api id")

API_HASH: str = gtnv("API_HASH")

if not API_HASH:
    raise ValueError("No api hash")

API_NAME: str = gtnv("API_NAME") or "test_client"


TRIGGER_WORDS: list = [
    "прекрасно",
    "ожидать",
]

MSG_1_TEXT: str = "Сообщение 1"
MSG_1_DELAY: int = 6 * 60

MSG_2_TEXT: str = "Сообщение 2"
MSG_2_DELAY: int = 39 * 60

MSG_3_TEXT: str = "Сообщение 3"
MSG_3_DELAY: int = 26 * 60 * 60

TRIGGER_MESSAGE = "Триггер"
