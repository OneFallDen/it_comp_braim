from fastapi import routing, Depends
from sqlalchemy.orm import Session


from sql.db import get_db
from controllers.reg_controller import reg_user
from models import schemas


router = routing.APIRouter()


@router.post('/registration', tags=['registration'], status_code=201)
async def registration_user(user: schemas.AccountReg, db: Session = Depends(get_db)):
    return reg_user(user.firstName, user.lastName, user.email, user.password, db)
