from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Logs, SaveCity


async def orm_save_city(session: AsyncSession, city: str, user_id: int):
    """Сохранение города в БД"""
    result = await session.execute(select(SaveCity).filter_by(user_id=user_id))
    existing_record = result.scalar_one_or_none()
    if existing_record:
        existing_record.city = city
    else:
        obj = SaveCity(user_id=user_id, city=city)
        session.add(obj)
    await session.commit()

 
async def orm_get_city(session: AsyncSession, user_id: int):
    """Получение сохраненного города для конкретного пользователя из БД"""
    result = await session.execute(select(SaveCity).filter_by(user_id=user_id))
    city = result.scalar_one_or_none()
    return city


async def orm_save_logs(session: AsyncSession, user_id: int, request: str, response: str):
    """Сохранени логов в БД"""
    obj = Logs(user_id=user_id, request=request, response=response)
    session.add(obj)
    await session.commit()

  
async def orm_get_all_logs(session: AsyncSession):
    """Получение всех логов из БД"""
    result = await session.execute(select(Logs))
    return result.scalars()


async def orm_get_user_log(session: AsyncSession, user_id: int):
    """Получение всех логов конкретного пользователя"""
    result = await session.execute(select(Logs).where(Logs.user_id == user_id))
    return result.scalars()
