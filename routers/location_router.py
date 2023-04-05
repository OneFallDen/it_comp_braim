from fastapi import routing, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Union
from datetime import datetime


from models import schemas
from controllers.validation_controller import check_roles
from sql.db import get_db
from controllers.reg_controller import get_current_account
from sql import models
from controllers.location_controller import get_loc_info, search_loc, point_visit_add, point_visit_update, \
    visited_point_delete, location_add, location_update, location_delete


router = routing.APIRouter()


@router.get('/animals/{animalId}/locations', tags=['location'])
async def location_search(animalId: int, startDateTime: Union[datetime, None] = None, endDateTime: Union[datetime, None]
= None, froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10,
                           db: Session = Depends(get_db), account: Union[models.Account, None] = Depends(get_current_account)):
    return search_loc(animalId, startDateTime, endDateTime, froom, size, db)


@router.put('/animals/{animalId}/locations', tags=['location'])
async def visit_point_update(animalId: int, location: schemas.UpdatePoint, db: Session = Depends(get_db),
                    user: models.Account = Depends(get_current_account)):
    if not user:
        raise HTTPException(status_code=401)
    return point_visit_update(animalId, location.visitedLocationPointId, location.locationPointId, db)


@router.delete('/animals/{animalId}/locations/{visitedPointId}', tags=['location'])
async def delete_visited_point(animalId: int, visitedPointId: int, db: Session = Depends(get_db),
                               user: models.Account = Depends(get_current_account)):
    if not user:
        raise HTTPException(status_code=401)
    return visited_point_delete(animalId, visitedPointId, db)


@router.post('/animals/{animalId}/locations/{pointId}', tags=['location'], status_code=201)
async def visit_point_add(animalId: int, pointId: int, db: Session = Depends(get_db),
                    user: models.Account = Depends(get_current_account)):
    if not user:
        raise HTTPException(status_code=401)
    return point_visit_add(animalId, pointId, db)


@router.get('/locations/{pointId}', tags=['location'])
async def get_location_info(pointId: int, db: Session = Depends(get_db),
                            account: Union[models.Account, None] = Depends(get_current_account)):
    return get_loc_info(pointId, db)


@router.post('/locations', tags=['location'], status_code=201)
async def add_location(location: schemas.Location, user: models.Account = Depends(get_current_account),
                       db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return location_add(location.latitude, location.longitude, user, db)


@router.delete('/locations/{pointId}', tags=['location'])
async def delete_location(pointId: int, user: models.Account = Depends(get_current_account),
                       db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN'])
    return location_delete(pointId, user, db)


@router.put('/locations/{pointId}', tags=['location'])
async def update_location(pointId: int, location: schemas.Location,
                       user: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return location_update(pointId, location.latitude, location.longitude, user, db)
