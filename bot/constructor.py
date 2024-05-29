from settings import logger, API_ID, API_HASH, API_NAME
from pyrogram import Client, idle
from handlers import begin_chat_handler, cool_or_wait_message_handler
from db import create_db, engine, Base


logger.debug("Making Client instance with user api_id and api_hash")
app = Client(name=API_NAME, api_id=API_ID, api_hash=API_HASH)

logger.debug(f"Adding {cool_or_wait_message_handler}")
app.add_handler(cool_or_wait_message_handler, group=1)
logger.debug(f"Adding {begin_chat_handler}")
app.add_handler(begin_chat_handler, group=2)


async def main(client):
    logger.info(f"Starting bot: API_NAME={API_NAME}, API_ID={API_ID}")
    try:
        await create_db(async_db_engine=engine, db_base=Base)
        await client.start()

        await idle()
        logger.info(f"Bot stopped working")
        await client.stop()
    except Exception as e:
        logger.error(f"{e}")


