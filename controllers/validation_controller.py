from typing import List
from fastapi import HTTPException
import re


pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"


def check_roles(role: str, roles: List):
    if not role in roles:
        raise HTTPException(status_code=403)


def valid_string(string: str):
    if not string:
        raise HTTPException(status_code=400)
    if string.strip() == '':
        raise HTTPException(status_code=400)


def valid_email_pattern(email: str):
    if re.match(pattern, email) is None:
        raise HTTPException(status_code=400)


def valid_roles(role: str):
    roles = ["ADMIN", "CHIPPER", "USER"]
    if not role in roles:
        raise HTTPException(status_code=400)


def valid_int(integer: int):
    if not integer:
        raise HTTPException(status_code=400)
    if integer <= 0:
        raise HTTPException(status_code=400)


def valid_location(latitude: float, longitude: float):
    if latitude == 0:
        latitude = 0.99999999
    if longitude == 0:
        longitude = 0.99999999
    if not latitude:
        raise HTTPException(status_code=400)
    if latitude < -90:
        raise HTTPException(status_code=400)
    if latitude > 90:
        raise HTTPException(status_code=400)
    if not longitude:
        raise HTTPException(status_code=400)
    if longitude < -180:
        raise HTTPException(status_code=400)
    if longitude > 180:
        raise HTTPException(status_code=400)
