from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum


class Account(BaseModel):
    id: int
    firstname: str
    lastname: str
    password: str
    email: EmailStr
