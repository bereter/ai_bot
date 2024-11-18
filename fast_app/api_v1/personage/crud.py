from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Personage
from sqlalchemy import select
from sqlalchemy.engine import Result


# получение статуса от персонажа, отдает последний из списка
async def get_personage(session: AsyncSession, personage: str) -> Personage | None:
    stmt = select(Personage).filter_by(themes=personage).order_by(Personage.id.desc())
    result: Result = await session.execute(stmt)
    personage_status = result.scalars().first()
    return personage_status