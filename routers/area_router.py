from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db
from controllers.area_controller import add_new_area
from sql import models
from models import schemas
from controllers.validation_controller import check_roles
from controllers.reg_controller import get_current_account


router = routing.APIRouter()


@router.post('/areas', tags=['areas'])
async def add_area(area: schemas.AreaToAdd, db: Session = Depends(get_db),
                   account: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(account.role, ['ADMIN'])
    return add_new_area(area, db)
