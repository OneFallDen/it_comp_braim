from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql import models
from models import schemas

"""
    ACCOUNT
"""


def get_account(account_id: int, db: Session):
    result = db.execute(select(models.Account).where(models.Account.id == account_id)).first()
    return {
        'id': result[0].id,
        'firstname': result[0].firstname,
        'lastname': result[0].lastname,
        'email': result[0].email
    }


def check_email(email: str, db: Session):
    result = db.execute(select(models.Account).where(models.Account.email == email)).first()
    return result[0].id


def signup_user(firstname: str, lastname: str, email: str, password: str, db: Session):
    db_user = models.Account(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


def search_account(firstname, lastname, email, froom, size, db: Session):
    result = db.execute(select(models.Account)).scalars().all()
    accs = []
    accs_to_send = []
    to_remove = []
    i = 0
    j = 0
    if firstname:
        for res in result:
            if firstname in res.firstname:
                accs.append({
                    'id': res.id,
                    'firstName': res.firstname,
                    'lastName': res.lastname,
                    'email': res.email
                })
    if lastname:
        for acc in accs:
            if not (lastname in acc['lastName']):
                to_remove.append(acc)
        for tr in to_remove:
            accs.remove(tr)
        to_remove.clear()
    if email:
        for acc in accs:
            if not (email in acc['email']):
                to_remove.append(acc)
        for tr in to_remove:
            accs.remove(tr)
        to_remove.clear()
    for acc in accs:
        if j != froom:
            j += 1
        else:
            if i == size:
                break
            accs_to_send.append(acc)
            i += 1
    return accs_to_send


"""
    ANIMAL
"""


def get_animal(animal_id: int, db: Session):
    result = db.execute(select(models.Animal).where(models.Animal.id == animal_id)).first()
    result_types = db.execute(select(models.AnimalTypes).where(models.AnimalTypes.animal_id == animal_id)).scalars().all()
    result_locs = db.execute(select(models.VisitedLocations).where(models.VisitedLocations.animal_id == animal_id)).\
        scalars().all()
    animal_types = []
    animal_locs = []
    for res in result_locs:
        animal_locs.append(res.loc_id)
    for res in result_types:
        animal_types.append(res.type_id)
    return {
        'id': animal_id,
        'animalsTypes': animal_types,
        "weight": result[0].weight,
        "length": result[0].length,
        "height": result[0].height,
        "gender": result[0].gender,
        "lifeStatus": result[0].lifestatus,
        "chippingDateTime": result[0].chippingdatetime,
        "chipperId": result[0].chipperid,
        "chippingLocationId": result[0].chippinglocationid,
        "visitedLocations": animal_locs,
        "deathDateTime": result[0].deathdatetime
    }


def get_type(type_id: int, db: Session):
    result = db.execute(select(models.Types).where(models.Types.id == type_id)).first()
    return result[0]


"""
    Location
"""


def get_location(point_id: int, db: Session):
    result = db.execute(select(models.Locations).where(models.Locations.id == point_id)).first()
    return {
        'id': result[0].id,
        'latitude': result[0].latitude,
        'longitude': result[0].longitude
    }


def loc_search(animalId: int, startDateTime, endDateTime, froom, size, db: Session):
    result = db.execute(select(models.VisitedLocations)).scalars().all()
    locs = []
    locs_to_send = []
    to_remove = []
    i = 0
    j = 0
    for res in result:
        locs.append({
            'id': res.id,
            'dateTimeOfVisitLocationPoint': res.date_of_visit,
            'locationPointId': res.loc_id
        })
    if startDateTime:
        try:
            for loc in locs:
                if startDateTime > loc['dateTimeOfVisitLocationPoint']:
                    to_remove.append(loc)
            for tr in to_remove:
                locs.remove(tr)
            to_remove.clear()
        except:
            raise HTTPException(status_code=400)
    if endDateTime:
        try:
            for loc in locs:
                if endDateTime < loc['dateTimeOfVisitLocationPoint']:
                    to_remove.append(loc)
            for tr in to_remove:
                locs.remove(tr)
            to_remove.clear()
        except:
            raise HTTPException(status_code=400)
    for loc in locs:
        if j != froom:
            j += 1
        else:
            if i == size:
                break
            locs_to_send.append(loc)
            i += 1
    return locs_to_send
