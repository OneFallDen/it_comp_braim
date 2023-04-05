from typing import List
from fastapi import HTTPException


def check_roles(role: str, roles: List):
    if not role in roles:
        raise HTTPException(status_code=403)
