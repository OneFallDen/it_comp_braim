from fastapi import routing, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic

from sql.db import get_db
from auth.auth import security_for_reg
from controllers.reg_controller import reg_user, get_current_account
from models import schemas
from sql import models
from typing import Union


router = routing.APIRouter()


@router.post('/registration', tags=['registration'], status_code=201)
async def registration_user(user: schemas.AccountReg, db: Session = Depends(get_db), account: Union[HTTPBasic, None] = Depends(security_for_reg)):
    if account:
        raise HTTPException(status_code=403)
    return reg_user(user.firstName, user.lastName, user.email, user.password, db)
