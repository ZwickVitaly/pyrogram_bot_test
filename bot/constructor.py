from db import Base, create_db_sync, engine
from handlers import begin_chat_handler, cool_or_wait_message_handler
from helpers import (
    sync_get_api_session_string,
    sync_export_api_session_string,
    sync_set_api_session_string,
)
from pyrogram import Client, idle
from settings import API_HASH, API_ID, API_NAME, logger, BASE_DIR

create_db_sync(async_db_engine=engine, db_base=Base)

api_string = sync_get_api_session_string()

logger.debug("Making Client instance with user api_id and api_hash")
app = Client(
    name=API_NAME, api_id=API_ID, api_hash=API_HASH, workdir=BASE_DIR, in_memory=True, session_string=api_string
)

if not api_string:
    api_string = sync_export_api_session_string(app)
    sync_set_api_session_string(api_string)
    app = Client(
        name=API_NAME, api_id=API_ID, api_hash=API_HASH, workdir=BASE_DIR, in_memory=True, session_string=api_string
    )


logger.debug(f"Adding {cool_or_wait_message_handler}")
app.add_handler(cool_or_wait_message_handler, group=1)
logger.debug(f"Adding {begin_chat_handler}")
app.add_handler(begin_chat_handler, group=2)


async def main(client):
    logger.info(f"Starting bot: API_NAME={API_NAME}, API_ID={API_ID}")
    await client.start()
    await idle()
    logger.info(f"Bot stopped working")
    await client.stop()

