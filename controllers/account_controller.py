from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union

from sql.crud import get_account, search_account


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
