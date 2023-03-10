from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db
from controllers.account_controller import get_acc_info, acc_search


router = routing.APIRouter()


@router.get('/accounts/search', tags=['account'])
async def account_search(firstname: Union[str, None] = None, lastName: Union[str, None] = None, email: Union[str, None]
= None, froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10,
                           db: Session = Depends(get_db)):
    return acc_search(firstname, lastName, email, froom, size, db)


@router.get('/accounts/{accountId}', tags=['account'])
async def get_account_info(accountId: int, db: Session = Depends(get_db)):
    return get_acc_info(accountId, db)
