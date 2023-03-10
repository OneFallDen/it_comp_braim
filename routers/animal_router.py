from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union
from datetime import datetime


from sql.db import get_db
from controllers.animal_controller import get_anim_info, get_info_type, search_anim


router = routing.APIRouter()


@router.get('/animals/search', tags=['animal'])
async def animal_search(startDateTime: Union[datetime, None] = None, endDateTime: Union[datetime, None] = None,
chipperId: Union[int, None] = None, chippingLocationId: Union[int, None] = None, lifeStatus: Union[str, None] = None,
gender: Union[str, None] = None,
froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10, db: Session = Depends(get_db)):
    return search_anim(startDateTime, endDateTime, chipperId, chippingLocationId, lifeStatus, gender, froom, size, db)


@router.get('/animal/{animalId}', tags=['animal'])
async def get_animal_info(animalId: int, db: Session = Depends(get_db)):
    return get_anim_info(animalId, db)


@router.get('/animals/types/{typeId}', tags=['animal'])
async def get_type_info(typeId: int, db: Session = Depends(get_db)):
    return get_info_type(typeId, db)
