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
