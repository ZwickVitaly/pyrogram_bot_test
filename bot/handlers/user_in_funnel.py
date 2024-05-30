from helpers import update_user_status, user_is_alive
from pyrogram import filters
from pyrogram.errors import UserDeactivated, UserIsBlocked
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from settings import TRIGGER_MESSAGE, TRIGGER_WORDS, logger


async def cool_or_wait_message(client, message: Message):
    logger.debug(f"User: {message.from_user.id} posted trigger word")
    user_alive = await user_is_alive(message.from_user.id)
    if user_alive:
        logger.debug(f"User: {message.from_user.id} is alive, updating status")
        await update_user_status(user_id=message.from_user.id, new_status="finished")
        logger.debug(
            f"User: {message.from_user.id} status updated, stopping propagation"
        )
        message.stop_propagation()
        try:
            logger.debug(
                f"Trying to reply to user: {message.from_user.id} with TRIGGER_MESSAGE"
            )
            await message.reply(TRIGGER_MESSAGE)
        except (UserIsBlocked, UserDeactivated):
            logger.debug(
                f"User: {message.from_user.id} blocked us. Updating status to 'dead'"
            )
            await update_user_status(user_id=message.from_user.id, new_status="dead")
    else:
        logger.debug(
            f"User {message.from_user.id} is not 'alive' or not found, passing to next filter"
        )
        return


logger.debug("Generating pattern for trigger-words filter")
pattern = rf"{'|'.join(TRIGGER_WORDS)}"

logger.debug("Making MessageHandler instance for cool_or_wait_message func")
cool_or_wait_message_handler = MessageHandler(
    cool_or_wait_message,
    filters=filters.regex(pattern=pattern, flags=2) & filters.private,
)
