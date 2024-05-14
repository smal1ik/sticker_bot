from app.database.models import User, async_session
from sqlalchemy import select, BigInteger


async def add_user(tg_id: int, first_name: str, username):
    """
    Функция добавляет пользователя в БД
    """
    tg_id = int(tg_id)
    async with async_session() as session:
        session.add(User(tg_id=tg_id, first_name=first_name, username=username))
        await session.commit()


async def get_user(tg_id: int):
    """
    Получаем пользователя по tg_id
    """
    tg_id = int(tg_id)
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result