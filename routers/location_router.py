from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union
from datetime import datetime


from sql.db import get_db
from controllers.location_controller import get_loc_info, search_loc


router = routing.APIRouter()


@router.get('/animals/{animalId}/locations', tags=['location'])
async def location_search(animalId: int, startDateTime: Union[datetime, None] = None, endDateTime: Union[datetime, None]
= None, froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10,
                           db: Session = Depends(get_db)):
    return search_loc(animalId, startDateTime, endDateTime, froom, size, db)


@router.get('/locations/{pointId}', tags=['location'])
async def get_location_info(pointId: int, db: Session = Depends(get_db)):
    return get_loc_info(pointId, db)
