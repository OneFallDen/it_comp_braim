from fastapi import routing, Depends
from sqlalchemy.orm import Session


from sql.db import get_db
from controllers.reg_controller import reg_user


router = routing.APIRouter()


@router.post('/registration', tags=['registration'], status_code=201)
async def registration_user(firstname: str, lastname: str, email: str, password: str, db: Session = Depends(get_db)):
    return reg_user(firstname, lastname, email, password, db)
