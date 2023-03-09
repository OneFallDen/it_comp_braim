from fastapi import routing, Depends
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db


router = routing.APIRouter()


@router.get('/accounts/{accountId}', tags=['account'])
async def get_account_info(accountId: int, db: Session = Depends(get_db)):
    return accountId
