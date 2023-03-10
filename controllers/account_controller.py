from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union
import re

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
from sql.crud import get_account, search_account, check_email, acc_update
from sql import models
from auth.auth import encode_password


def get_acc_info(account_id: int, db: Session):
    if not account_id:
        raise HTTPException(status_code=400)
    if account_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_account(account_id, db)
    except:
        raise HTTPException(status_code=404)


def acc_search(firstname, lastname, email, froom, size, db: Session):
    if froom < 0:
        raise HTTPException(status_code=400)
    if size <= 0:
        raise HTTPException(status_code=400)
    return search_account(firstname, lastname, email, froom, size, db)


def update_acc(accountId: int, firstname: str, lastname: str, email: str, password: str, db: Session,
               user: models.Account):
    if user.id != accountId:
        raise HTTPException(status_code=403)
    try:
        get_account(accountId, db)
    except:
        raise HTTPException(status_code=404)
    s = 0
    try:
        s = check_email(email, db)
    except:
        d = 1
    if s > 0:
        raise HTTPException(status_code=409)
    if not firstname:
        raise HTTPException(status_code=400)
    if firstname.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if not lastname:
        raise HTTPException(status_code=400)
    if lastname.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if not email:
        raise HTTPException(status_code=400)
    if email.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if re.match(pattern, email) is None:
        raise HTTPException(status_code=400)
    if not password:
        raise HTTPException(status_code=400)
    if password.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    hashed_password = encode_password(password)
    return acc_update(accountId, firstname, lastname, email, hashed_password, db)
