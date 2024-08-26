from sqlalchemy.orm import Session

from city_app.schemas import CityCreate, CityList
from models import City


def get_city(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_all_cities(db: Session):
    return db.query(City).all()


def create_city(db: Session, city: CityCreate):
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
