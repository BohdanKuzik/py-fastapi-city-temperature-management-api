from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float,
)

from database import Base


class Temperature(Base):
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
