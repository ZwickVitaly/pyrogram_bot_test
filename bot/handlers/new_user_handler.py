from asyncio import sleep

from db import User, async_session
from helpers import merge_user_status, update_user_status, user_is_alive
from pyrogram import Client, filters
from pyrogram.errors import UserDeactivated, UserIsBlocked
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from settings import (
    MSG_1_DELAY,
    MSG_1_TEXT,
    MSG_2_DELAY,
    MSG_2_TEXT,
    MSG_3_DELAY,
    MSG_3_TEXT,
    logger,
)
from sqlalchemy import select


async def begin_chat(client: Client, message: Message):
    logger.debug(f"Message from user: {message.from_user.id}")
    try:
        async with async_session() as session:
            async with session.begin():
                logger.debug(f"Looking for user: {message.from_user.id}")
                user_q = await session.execute(
                    select(User).where(User.id == message.from_user.id)
                )
                user: User = user_q.scalar_one_or_none()
                if not user:
                    logger.debug(f"Creating new user: {message.from_user.id}")
                    user = User(id=message.from_user.id)
                    session.add(user)
                    await session.commit()
                else:
                    logger.debug(f"User: {message.from_user.id} exists, no response")
                    return
        logger.debug(f"Wating {MSG_1_DELAY} seconds")
        await sleep(MSG_1_DELAY)
        logger.debug(f"Sending first message to user: {message.from_user.id}")
        await message.reply(MSG_1_TEXT)

        logger.debug(f"Wating for {MSG_2_DELAY} seconds")
        await sleep(MSG_2_DELAY)
        logger.debug(
            f"Checking if user: {message.from_user.id} is still 'alive' after first message"
        )
        user_still_alive = await user_is_alive(message.from_user.id)
        if user_still_alive:
            logger.debug(f"Sending second message to user: {message.from_user.id}")
            await message.reply(MSG_2_TEXT)
        else:
            logger.debug(f"User: {message.from_user.id} is not 'alive', passing")
            return

        logger.debug(f"Wating for {MSG_3_DELAY} seconds")
        await sleep(MSG_3_DELAY)
        logger.debug(
            f"Checking if user: {message.from_user.id} is still 'alive' after second message"
        )
        user_still_alive = await user_is_alive(message.from_user.id)
        if user_still_alive:
            logger.debug(f"Sending third message to user: {message.from_user.id}")
            await message.reply(MSG_3_TEXT)
            logger.debug(
                f"Updating user's: {message.from_user.id} status to 'finished'"
            )
            await update_user_status(
                user_id=message.from_user.id, new_status="finished"
            )
        else:
            return

    except (UserIsBlocked, UserDeactivated):
        logger.error(
            f"User: {message.from_user.id} is blocked us or deactivated account. Changing status to 'dead'"
        )
        await merge_user_status(user_id=message.from_user.id, new_status="dead")


logger.debug("Making MessageHandler instance for begin_chat func")
begin_chat_handler = MessageHandler(begin_chat, filters=filters.text & filters.private)
