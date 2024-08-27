from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from city_app import crud
from city_app.schemas import CityList, CityCreate
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/cities/", response_model=list[CityList])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@app.get("/cities/{city_id}/", response_model=CityList)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}/", response_model=CityList)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/cities/", response_model=CityList)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.patch("/cities/{city_id}/", response_model=CityList)
def update_city(city_id: int, city_data: CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city_data=city_data)
