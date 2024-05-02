from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from .models import *
from typing import Union
import datetime
from aiogram import types, Bot
from db.base import get_session


async def get_user(id:str) -> User:
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        return user
    
async def create_user(user: types.User) -> User:
    async with await get_session() as session:
        session.add(user)
        await session.commit()

async def delete_user(id: str):
    async with await get_session() as session:
        await session.delete(await get_user(id=id))
        await session.commit()

async def get_image(name: str) -> str:
    async with await get_session() as session:
        image = await session.execute(select(Image).where(Image.name == name))
        image = image.scalars().first()
        return image
    
async def create_image(name: str, id: str) -> Image:
    async with await get_session() as session:
        image = Image(name=name, id=id)
        session.add(image)
        await session.commit()
        

async def get_moderation_candidate() -> User:
    async with await get_session() as session:
        candidates = await session.execute(select(User).where(User.moderated == False))
        candidates = candidates.scalars().first()
        return candidates
    
async def accept_candidate(id:int):
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        user.moderated = True
        await session.commit()

async def send_mailing(bot:Bot, text: str):
    async with await get_session() as session:
        users = await session.execute(select(User))
        users = users.scalars().all()
        for user in users:
            await bot.send_message(user.id, text=text)

async def get_admins() -> list[int]:
    async with await get_session() as session:
        admins = await session.execute(select(Admin))
        admins = admins.scalars().all()
        return [admin.id for admin in admins]
