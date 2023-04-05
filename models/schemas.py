from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Union


class Account(BaseModel):
    id: int
    firstname: str
    lastname: str
    password: str
    email: EmailStr


class AccountWithRoles(Account):
    role: str


class UpdatePoint(BaseModel):
    visitedLocationPointId: int
    locationPointId: int


class AddType(BaseModel):
    type: Union[str, None]


class Location(BaseModel):
    latitude: Union[float, None]
    longitude: Union[float, None]


class AccountReg(BaseModel):
    firstName: Union[str, None]
    lastName: Union[str, None]
    email: Union[str, None]
    password: Union[str, None]


class NewAnimal(BaseModel):
    animalTypes: Union[List[int], None]
    weight: Union[float, None]
    length: Union[float, None]
    height: Union[float, None]
    gender: Union[str, None]
    chipperId: Union[int, None]
    chippingLocationId: Union[int, None]


class UpdateAnimal(BaseModel):
    weight: Union[float, None]
    length: Union[float, None]
    height: Union[float, None]
    gender: Union[str, None]
    lifeStatus: Union[str, None]
    chipperId: Union[int, None]
    chippingLocationId: Union[int, None]


class UpdateAnimalTypes(BaseModel):
    oldTypeId: Union[int, None]
    newTypeId: Union[int, None]


class Roles(str, Enum):
    ADMIN: "ADMIN"
    CHIPPER: "CHIPPER"
    USER: "USER"
