from fastapi import routing, Depends, Query, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db
from sql import models
from controllers.account_controller import get_acc_info, acc_search, update_acc, delete_acc, add_acc_by_admin
from controllers.reg_controller import get_current_account
from models import schemas
from controllers.validation_controller import check_roles
from auth.auth import security


router = routing.APIRouter()


@router.put('/accounts/{accountId}', tags=['account'])
async def update_account(accountId: int, account: schemas.UpdateAccount,
                         db: Session = Depends(get_db),
                         user: models.Account = Depends(get_current_account)):
    if accountId != user.id:
        check_roles(user.role, ['ADMIN'])
    return update_acc(accountId, account.firstName, account.lastName, account.email, account.password, account.role, db)


@router.delete('/accounts/{accountId}', tags=['account'])
async def delete_account(accountId: int,
                         db: Session = Depends(get_db),
                         user: models.Account = Depends(get_current_account)):
    if user.id != accountId:
        check_roles(user.role, ['ADMIN'])
    return delete_acc(accountId, db, user)


@router.get('/accounts/search', tags=['account'])
async def account_search(firstName: Union[str, None] = None, lastName: Union[str, None] = None, email: Union[str, None]
= None, froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10,
                           db: Session = Depends(get_db), user: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(user.role, ['ADMIN'])
    return acc_search(firstName, lastName, email, froom, size, db)


@router.get('/accounts/{accountId}', tags=['account'])
async def get_account_info(accountId: int, db: Session = Depends(get_db), account: Union[models.Account, None] = Depends(get_current_account)):
    if accountId != account.id:
        check_roles(account.role, ['ADMIN'])
    return get_acc_info(accountId, db)


@router.post('/accounts', tags=['account'])
async def add_account(user: schemas.AccountRegByAdmin, db: Session = Depends(get_db),
                      account: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(account.role, ['ADMIN'])
    return add_acc_by_admin(user, db)
