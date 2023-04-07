from fastapi import routing, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Union, List
from datetime import datetime


from sql.db import get_db
from controllers.animal_controller import get_anim_info, get_info_type, search_anim, animal_type_add, animal_type_update\
    , animal_type_delete, animal_add, animal_update, animal_delete, type_to_animal_add, animal_types_update, type_from_animal_delete
from sql import models
from controllers.reg_controller import get_current_account
from models import schemas
from controllers.validation_controller import check_roles


router = routing.APIRouter()


@router.get('/animals/search', tags=['animal'])
async def animal_search(startDateTime: Union[datetime, None] = None, endDateTime: Union[datetime, None] = None,
chipperId: Union[int, None] = None, chippingLocationId: Union[int, None] = None, lifeStatus: Union[str, None] = None,
gender: Union[str, None] = None,
froom: Union[int, None] = Query(default=0, alias="from"), size: Union[int, None] = 10, db: Session = Depends(get_db),
                        account: Union[models.Account, None] = Depends(get_current_account)):
    return search_anim(startDateTime, endDateTime, chipperId, chippingLocationId, lifeStatus, gender, froom, size, db)


@router.get('/animals/{animalId}', tags=['animal'])
async def get_animal_info(animalId: int, db: Session = Depends(get_db), account: Union[models.Account, None] = Depends(get_current_account)):
    return get_anim_info(animalId, db)


@router.post('/animals', tags=['animal'], status_code=201)
async def add_animal(animal: schemas.NewAnimal, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return animal_add(animal.animalTypes, animal.weight, animal.length, animal.height, animal.gender, animal.chipperId, animal.chippingLocationId, user, db)


@router.put('/animals/{animalId}', tags=['animal'])
async def update_animal(animalId: int, animal: schemas.UpdateAnimal, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return animal_update(animalId, animal.weight, animal.length, animal.height, animal.gender, animal.lifeStatus, animal.chipperId, animal.chippingLocationId, user, db)


@router.delete('/animals/{animalId}', tags=['animal'])
async def delete_animal(animalId: int, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN'])
    return animal_delete(animalId, user, db)


@router.post('/animals/{animalId}/types/{typeId}', tags=['animal_type'], status_code=201)
async def add_type_to_animal(animalId: int, typeId: int, user: models.Account = Depends(get_current_account),
                     db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return type_to_animal_add(animalId, typeId, user, db)


@router.get('/animals/types/{typeId}', tags=['animal_type'])
async def get_type_info(typeId: int, db: Session = Depends(get_db), account: Union[models.Account, None] = Depends(get_current_account)):
    return get_info_type(typeId, db)


@router.post('/animals/types', tags=['animal_type'], status_code=201)
async def add_animal_type(type: schemas.AddType, user: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return animal_type_add(type.type, db)


@router.put('/animals/{animalId}/types', tags=['animal_type'])
async def update_animal_types(animalId: int, animal: schemas.UpdateAnimalTypes, user: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return animal_types_update(animalId, animal.oldTypeId, animal.newTypeId, user, db)


@router.delete('/animals/{animalId}/types/{typeId}', tags=['animal_type'])
async def delete_type_from_animal(animalId: int, typeId: int, user: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return type_from_animal_delete(animalId, typeId, db)


@router.put('/animals/types/{typeId}', tags=['animal_type'])
async def update_animal_type(typeId: int, type: schemas.AddType, user: models.Account = Depends(get_current_account),
                          db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN', 'CHIPPER'])
    return animal_type_update(typeId, type.type, user, db)


@router.delete('/animals/types/{typeId}', tags=['animal_type'])
async def delete_animal_type(typeId: int, user: models.Account = Depends(get_current_account),
                          db: Session = Depends(get_db)):
    check_roles(user.role, ['ADMIN'])
    return animal_type_delete(typeId, user, db)
