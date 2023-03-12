from fastapi import routing, Depends, HTTPException
from sqlalchemy.orm import Session

from sql.db import get_db
from controllers.reg_controller import reg_user, get_current_account
from models import schemas
from sql import models


router = routing.APIRouter()


@router.post('/registration', tags=['registration'], status_code=201)
async def registration_user(user: schemas.AccountReg, account: models.Account = Depends(get_current_account) , db: Session = Depends(get_db)):
    if account:
        raise HTTPException(status_code=403)
    return reg_user(user.firstName, user.lastName, user.email, user.password, db)
