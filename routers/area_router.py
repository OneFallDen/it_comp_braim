from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union


from sql.db import get_db
from controllers.area_controller import add_new_area, get_area_by_id, delete_area_by_id, update_area_by_id
from sql import models
from models import schemas
from controllers.validation_controller import check_roles
from controllers.reg_controller import get_current_account


router = routing.APIRouter()


@router.post('/areas', tags=['areas'], status_code=201)
async def add_area(area: schemas.AreaToAdd, db: Session = Depends(get_db),
                   account: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(account.role, ['ADMIN'])
    return add_new_area(area, db)


@router.get('/areas/{areaId}', tags=['areas'])
async def get_area(areaId: int, db: Session = Depends(get_db),
                   account: Union[models.Account, None] = Depends(get_current_account)):
    return get_area_by_id(areaId, db)


@router.delete('/areas/{areaId}', tags=['areas'])
async def delete_area(areaId: int, db: Session = Depends(get_db),
                      account: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(account.role, ['ADMIN'])
    delete_area_by_id(areaId, db)


@router.put('/areas/{areaId}', tags=['areas'])
async def update_area(areaId: int, area: schemas.AreaToAdd, db: Session = Depends(get_db),
                      account: Union[models.Account, None] = Depends(get_current_account)):
    check_roles(account.role, ['ADMIN'])
    return update_area_by_id(areaId, area, db)
