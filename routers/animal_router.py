from fastapi import routing, Depends, Query
from sqlalchemy.orm import Session
from typing import Union, List
from datetime import datetime


from sql.db import get_db
from controllers.animal_controller import get_anim_info, get_info_type, search_anim, animal_type_add, animal_type_update\
    , animal_type_delete, animal_add
from sql import models
from controllers.reg_controller import get_current_account
from models import schemas


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


@router.post('/animal', tags=['animal'], status_code=201)
async def add_animal(animal: schemas.NewAnimal, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    return animal_add(animal.animalTypes, animal.weight, animal.length, animal.height, animal.gender, animal.chipperId, animal.chippingLocationId, user, db)


@router.put('/animal', tags=['animal'])
async def update_animal(animal: schemas.UpdateAnimal, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    return animal_add(animal.weight, animal.length, animal.height, animal.gender, animal.chipperId, animal.chippingLocationId, user, db)


@router.get('/animals/types/{typeId}', tags=['animal_type'])
async def get_type_info(typeId: int, db: Session = Depends(get_db)):
    return get_info_type(typeId, db)


@router.post('/animals/types', tags=['animal_type'], status_code=201)
async def add_animal_type(type: str, user: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    return animal_type_add(type, user, db)


@router.put('/animals/types/{typeId}', tags=['animal_type'])
async def update_animal_type(typeId: int, type: str, user: models.Account = Depends(get_current_account),
                          db: Session = Depends(get_db)):
    return animal_type_update(typeId, type, user, db)


@router.delete('/animals/types/{typeId}', tags=['animal_type'])
async def delete_animal_type(typeId: int, user: models.Account = Depends(get_current_account),
                          db: Session = Depends(get_db)):
    return animal_type_delete(typeId, user, db)
