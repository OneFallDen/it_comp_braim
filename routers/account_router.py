from fastapi import routing, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db
from sql import models
from controllers.account_controller import get_acc_info, acc_search, update_acc, delete_acc
from controllers.reg_controller import get_current_account


router = routing.APIRouter()


@router.put('/accounts/{accountId}', tags=['account'])
async def update_account(accountId: int, firstname: str, lastname: str, email: str, password: str,
                         db: Session = Depends(get_db),
                         user: models.Account = Depends(get_current_account)):
    return update_acc(accountId, firstname, lastname, email, password, db, user)


@router.delete('/accounts/{accountId}', tags=['account'])
async def delete_account(accountId: int,
                         db: Session = Depends(get_db),
                         user: models.Account = Depends(get_current_account)):
    return delete_acc(accountId, db, user)


@router.get('/accounts/search', tags=['account'])
async def account_search(firstname: Union[str, None] = None, lastName: Union[str, None] = None, email: Union[str, None]
= None, froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10,
                           db: Session = Depends(get_db)):
    return acc_search(firstname, lastName, email, froom, size, db)


@router.get('/accounts/{accountId}', tags=['account'])
async def get_account_info(accountId: int, db: Session = Depends(get_db)):
    return get_acc_info(accountId, db)
