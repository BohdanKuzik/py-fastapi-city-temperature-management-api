from typing import Optional, Callable, Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import update, delete

from city_app.schemas import CityCreate
from city_app.models import City


async def get_city(db: AsyncSession, city_id: int) -> Optional[City]:
    query = select(City).where(City.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_all_cities(db: AsyncSession) -> Sequence[City]:
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def create_city(
        db: AsyncSession,
        city: CityCreate
) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_data: CityCreate
) -> Callable[[], int]:
    result = await db.execute(
        update(City)
        .where(City.id == city_id)
        .values(name=city_data.name, additional_info=city_data.additional_info)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return result.rowcount


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> Callable[[], int]:
    result = await db.execute(
        delete(City).where(City.id == city_id)
    )
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return result.rowcount
