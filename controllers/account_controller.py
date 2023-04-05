from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union


from sql.crud import get_account, search_account, check_email, acc_update, get_account_animal, acc_delete, add_account
from sql import models
from auth.auth import encode_password
from models import schemas
from controllers.validation_controller import valid_string, valid_email_pattern, valid_roles


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
    valid_string(firstname)
    valid_string(lastname)
    valid_string(email)
    valid_email_pattern(email)
    valid_string(password)
    hashed_password = encode_password(password)
    try:
        get_account(accountId, db)
    except:
        raise HTTPException(status_code=404)
    s = 0
    try:
        s = check_email(email, db)
    except:
        d = 1
    if s != accountId:
        if s > 0:
            raise HTTPException(status_code=409)
    return acc_update(accountId, firstname, lastname, email, hashed_password, db)


def delete_acc(accountId: int, db: Session, user: models.Account):
    if not accountId:
        raise HTTPException(status_code=400)
    if accountId <= 0:
        raise HTTPException(status_code=400)
    try:
        get_account(accountId, db)
    except:
        raise HTTPException(status_code=403)
    if user.id != accountId:
        raise HTTPException(status_code=403)
    s = 0
    try:
        res = get_account_animal(accountId, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=400)
    if accountId != user.id:
        raise HTTPException(status_code=403)
    acc_delete(accountId, db)
