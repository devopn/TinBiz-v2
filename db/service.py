from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from .models import *
from typing import Union
import datetime
from sqlalchemy import or_
from aiogram import types, Bot
from db.base import get_session
from sqlalchemy import delete


async def get_user(id:int) -> User:
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        return user
    
async def create_user(user: types.User) -> User:
    async with await get_session() as session:
        session.add(user)
        await session.commit()

async def update_user(id: str, **kwargs):
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        for key, value in kwargs.items():
            setattr(user, key, value)
        await session.commit()

async def delete_user(id: str):
    async with await get_session() as session:
        await session.delete(await get_user(id=id))
        await session.commit()

async def get_image(name: str) -> Image:
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

async def get_search(id:int) -> list[User]:
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()

        filters = user.filters
        ages = []
        fields = []
        # Age filtration
        for k, v in filters["age"].items():
            if v:
                left = int(k.split("-")[0])
                right = int(k.split("-")[1])
                for i in range(left, right+1):
                    ages.append(i)
        # Field filtration
        for k, v in filters["field"].items():
            if v:
                fields.append(k)

    
        searches = await session.execute(select(Search).where(
            Search.from_id == user.id
        ))
        searches = searches.scalars().all()
        searches_id = [search.to_id for search in searches]

        users = await session.execute(select(User).where(
            (User.active == True) & (User.moderated == True) & (User.age.in_(ages)) & (User.field.in_(fields)) & (User.id.not_in(searches_id)) & (User.id != user.id))
            )
        users = users.scalars().all()
        users = sorted(users, key=lambda x: x.city.lower() == user.city.lower(), reverse=False)
        return users[:10]
    
async def add_search(from_id:int, to_id:int):
    async with await get_session() as session:
        search = Search(from_id=from_id, to_id=to_id)
        session.add(search)
        await session.commit()

async def delete_search(from_id:int):
    async with await get_session() as session:
        statement = delete(Search).where(Search.from_id == from_id)
        await session.execute(statement)
        await session.commit()

async def get_unmoderate_count():
    async with await get_session() as session:
        users = await session.execute(select(User).where(User.moderated == False))
        users = users.scalars().all()
        return len(users)