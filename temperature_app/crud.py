from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_app.models import Temperature
from temperature_app.schemas import TemperatureCreate


async def get_all_temperatures(
        db: AsyncSession,
) -> Sequence[Temperature]:
    query = select(Temperature)
    result = await db.execute(query)

    return result.scalars().all()


async def get_temperature_by_city_id(
        db: AsyncSession,
        city_id: int,
) -> List[Temperature]:
    query = select(Temperature).where(
        Temperature.city_id == city_id
    )
    result = await db.execute(query)

    return result.scalars().first()


async def create_temperature(
        db: AsyncSession, temperature: TemperatureCreate
) -> Temperature:
    db_temperature = Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature
