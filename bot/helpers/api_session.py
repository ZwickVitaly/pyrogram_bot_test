from asyncio import get_event_loop

from pyrogram import Client
from sqlalchemy import select
from db import async_session, Session
from settings import API_NAME


async def get_api_session_string():
    async with async_session() as db_session:
        async with db_session.begin():
            session_q = await db_session.execute(select(Session).where(Session.api_name == API_NAME))
            api_session = session_q.scalar_one_or_none()
    if api_session:
        return api_session.session_string


def sync_get_api_session_string():
    api_session_string = get_event_loop().run_until_complete(get_api_session_string())
    return api_session_string


async def set_api_session_string(session_string: str):
    async with async_session() as db_session:
        async with db_session.begin():
            api_session = Session(session_string=session_string, api_name=API_NAME)
            await db_session.merge(api_session)
            await db_session.commit()


def sync_set_api_session_string(session_string: str):
    get_event_loop().run_until_complete(set_api_session_string(session_string))


async def export_api_session_string(app: Client):
    async with app:
        return await app.export_session_string()


def sync_export_api_session_string(app: Client):
    return get_event_loop().run_until_complete(export_api_session_string(app))
