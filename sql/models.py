import sys
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import DECIMAL
from datetime import datetime


from sql.database import engine

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


class Animal(Base):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(DECIMAL, nullable=False)
    length = Column(DECIMAL, nullable=False)
    height = Column(DECIMAL, nullable=False)
    gender = Column(String(255), nullable=False)
    lifestatus = Column(String(255), nullable=False)
    chippingdatetime = Column(DateTime(), nullable=False)
    chipperid = Column(Integer, nullable=False)
    chippinglocationid = Column(Integer, nullable=False)
    deathdatetime = Column(DateTime)

    animalTypes = relationship('AnimalTypes', backref='user')
    visitedLocations = relationship('VisitedLocations', backref='user')


class AnimalTypes(Base):
    __tablename__ = 'animal_types'

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    type = Column(String(255), nullable=False)


class VisitedLocations(Base):
    __tablename__ = 'visited_locations'

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    loc_id = Column(Integer, ForeignKey('locations.id'), nullable=False)


class Locations(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False)

    visitedLocations = relationship('VisitedLocations', backref='locations')


def create_db_and_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    if sys.argv[1] == 'createdb':
        create_db_and_tables()
    elif sys.argv[1] == 'dropdb':
        drop_tables()
