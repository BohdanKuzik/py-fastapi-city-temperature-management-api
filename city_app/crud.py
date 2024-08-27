from sqlalchemy.orm import Session

from city_app.schemas import CityCreate
from city_app.models import City


def get_city(db: Session, city_id: int):
    city = db.query(City).filter(City.id == city_id).first()
    return city


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


def update_city(db: Session, city_id: int, city_data: CityCreate):
    city = db.query(City).filter(City.id == city_id).first()
    city.name = city_data.name
    city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
