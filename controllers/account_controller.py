from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union


from sql.crud import get_account, search_account, check_email, acc_update, get_account_animal, acc_delete, add_account
from sql import models
from auth.auth import encode_password
from models import schemas
from controllers.validation_controller import valid_string, valid_email_pattern, valid_roles, valid_int


def add_acc_by_admin(user: schemas.AccountRegByAdmin, db: Session):
    valid_string(user.firstName)
    valid_string(user.lastName)
    valid_string(user.email)
    valid_email_pattern(user.email)
    valid_string(user.password)
    valid_roles(user.role)
    hashed_password = encode_password(user.password)
    s = 0
    try:
        s = check_email(user.email, db)
    except:
        d = 1
    if s > 0:
        raise HTTPException(status_code=409)
    return add_account(user, db, hashed_password)


def get_acc_info(account_id: int, db: Session):
    valid_int(account_id)
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


def update_acc(accountId: int, firstname: str, lastname: str, email: str, password: str, role: str, db: Session):
    valid_int(accountId)
    valid_string(firstname)
    valid_string(lastname)
    valid_string(email)
    valid_email_pattern(email)
    valid_string(password)
    valid_roles(role)
    hashed_password = encode_password(password)
    try:
        get_account(accountId, db)
    except:
        raise HTTPException(status_code=404)
    return acc_update(accountId, firstname, lastname, email, hashed_password, role, db)


def delete_acc(accountId: int, db: Session, user: models.Account):
    valid_int(accountId)
    try:
        get_account(accountId, db)
    except:
        raise HTTPException(status_code=404)
    s = 0
    try:
        res = get_account_animal(accountId, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=400)
    acc_delete(accountId, db)
