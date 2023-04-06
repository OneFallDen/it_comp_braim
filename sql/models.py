import sys
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import DECIMAL
from datetime import datetime
from sql.database import SessionLocal
from passlib.context import CryptContext
import os


from sql.database import engine

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False, default="USER")


class Animal(Base):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(DECIMAL, nullable=False)
    length = Column(DECIMAL, nullable=False)
    height = Column(DECIMAL, nullable=False)
    gender = Column(String(255), nullable=False)
    lifestatus = Column(String(255), nullable=False)
    chippingdatetime = Column(DateTime(timezone=True), nullable=False)
    chipperid = Column(Integer, nullable=False)
    chippinglocationid = Column(Integer, nullable=False)
    deathdatetime = Column(DateTime)

    animalTypes = relationship('AnimalTypes', backref='user')
    visitedLocations = relationship('VisitedLocations', backref='user')


class AnimalTypes(Base):
    __tablename__ = 'animal_types'

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)


class Types(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), nullable=False)

    animalTypes = relationship('AnimalTypes', backref='types')


class VisitedLocations(Base):
    __tablename__ = 'visited_locations'

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    date_of_visit = Column(DateTime(timezone=True), default=datetime.now().astimezone().replace(microsecond=0))
    loc_id = Column(Integer, ForeignKey('locations.id'), nullable=False)


class Locations(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)

    visitedLocations = relationship('VisitedLocations', backref='locations')


class Area(Base):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    areaPoints = relationship('AreaPoints', backref='area')


class AreaPoints(Base):
    __tablename__ = 'area_points'
    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False)
    point_id = Column(Integer, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)


def create_db_and_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    if sys.argv[1] == 'createdb':
        create_db_and_tables()
        password = 'qwerty123'
        PASSWORD_SALT = os.environ['PASSWORD_SALT']
        hasher = CryptContext(schemes=['bcrypt'])
        passw = hasher.hash(password + PASSWORD_SALT)
        with SessionLocal() as db:
            db_admin = Account(
                firstname="adminFirstName",
                lastname="adminLastName",
                email="admin@simbirsoft.com",
                password=passw,
                role="ADMIN"
            )
            db.add(db_admin)
            db.commit()
            db.refresh(db_admin)
            db_chipper = Account(
                firstname="chipperFirstName",
                lastname="chipperLastName",
                email="chipper@simbirsoft.com",
                password=passw,
                role="CHIPPER"
            )
            db.add(db_chipper)
            db.commit()
            db.refresh(db_chipper)
            db_user = Account(
                firstname="userFirstName",
                lastname="userLastName",
                email="user@simbirsoft.com",
                password=passw,
                role="USER"
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

    elif sys.argv[1] == 'dropdb':
        drop_tables()
