from typing import Sequence

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from city_app import crud
from city_app.models import City
from city_app.schemas import CityList, CityCreate
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[CityList])
async def read_cities(db: AsyncSession = Depends(get_db)) -> Sequence[City]:
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=CityList)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}/", response_model=CityList)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=CityList)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.patch("/cities/{city_id}/", response_model=CityList)
async def update_city(city_id: int, city_data: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_city(db=db, city_id=city_id, city_data=city_data)
