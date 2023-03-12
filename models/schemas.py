from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List


class Account(BaseModel):
    id: int
    firstname: str
    lastname: str
    password: str
    email: EmailStr


class UpdatePoint(BaseModel):
    visitedLocationPointId: int
    locationPointId: int


class AddType(BaseModel):
    type: str


class Location(BaseModel):
    latitude: float
    longitude: float


class AccountReg(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str


class NewAnimal(BaseModel):
    animalTypes: List[int]
    weight: float
    length: float
    height: float
    gender: str
    chipperId: int
    chippingLocationId: int


class UpdateAnimal(BaseModel):
    weight: float
    length: float
    height: float
    gender: str
    lifeStatus: str
    chipperId: int
    chippingLocationId: int


class UpdateAnimalTypes(BaseModel):
    oldTypeId: int
    newTypeId: int
