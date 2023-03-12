import datetime

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


def get_user(username: str, db: Session):
    result = db.execute(select(models.Account).where(models.Account.email == username)).first()
    return result[0]


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


def acc_update(accountId: int, firstname: str, lastname: str, email: str, password: str, db: Session):
    db.query(models.Account).filter(models.Account.id == accountId).update(
        {
            models.Account.firstname: firstname,
            models.Account.lastname: lastname,
            models.Account.email: email,
            models.Account.password: password
        }
    )
    db.commit()
    return {
        'id': accountId,
        'firstName': firstname,
        'lastName': lastname,
        'email': email
    }


def get_account_animal(accountId: int, db: Session):
    result = db.execute(select(models.Animal).where(models.Animal.chipperid == accountId)).first()
    return result[0]


def acc_delete(accountId: int, db: Session):
    db.query(models.Account).filter(models.Account.id == accountId).delete()
    db.commit()


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


def anim_search(startDateTime, endDateTime, chipperId, chippingLocationId, lifeStatus, gender, froom, size, db: Session):
    result = db.execute(select(models.Animal)).scalars().all()
    anims = []
    anims_to_send = []
    to_remove = []
    i = 0
    j = 0
    for res in result:
        anims.append(get_animal(res.id, db))
    if startDateTime:
        try:
            for anim in anims:
                if startDateTime > anim['chippingDateTime']:
                    to_remove.append(anim)
            for tr in to_remove:
                anims.remove(tr)
            to_remove.clear()
        except:
            raise HTTPException(status_code=400)
    if endDateTime:
        try:
            for anim in anims:
                if endDateTime < anim['chippingDateTime']:
                    to_remove.append(anim)
            for tr in to_remove:
                anims.remove(tr)
            to_remove.clear()
        except:
            raise HTTPException(status_code=400)
    if chipperId:
        for anim in anims:
            if chipperId != anim['chipperId']:
                to_remove.append(anim)
        for tr in to_remove:
            anims.remove(tr)
        to_remove.clear()
    if chippingLocationId:
        for anim in anims:
            if not (chippingLocationId == anim['chippingLocationId']):
                to_remove.append(anim)
        for tr in to_remove:
            anims.remove(tr)
        to_remove.clear()
    if lifeStatus:
        for anim in anims:
            if lifeStatus != anim['lifeStatus']:
                to_remove.append(anim)
        for tr in to_remove:
            anims.remove(tr)
        to_remove.clear()
    if gender:
        for anim in anims:
            if gender != anim['gender']:
                to_remove.append(anim)
        for tr in to_remove:
            anims.remove(tr)
        to_remove.clear()
    for anim in anims:
        if j != froom:
            j += 1
        else:
            if i == size:
                break
            anims_to_send.append(anim)
            i += 1
    return anims_to_send


def get_animal_status(animalId: int, db: Session):
    result = db.execute(select(models.Animal).where(models.Animal.id == animalId)).first()
    return result[0].lifestatus


"""
    Location
"""


def delete_loc(pointId: int, db: Session):
    db.query(models.Locations).filter(models.Locations.id == pointId).delete()
    db.commit()


def check_loc_animal(pointId: int, db: Session):
    result = db.execute(select(models.VisitedLocations).where(models.VisitedLocations.loc_id == pointId)).first()
    return result[0]


def update_loc(pointId: int, latitude: float, longitude: float, db: Session):
    db.query(models.Locations).filter(models.Locations.id == pointId).update(
        {
            models.Locations.latitude: latitude,
            models.Locations.longitude: longitude
        }
    )
    db.commit()
    return {
        'id': pointId,
        'latitude': latitude,
        'longitude': longitude
    }


def add_loc(latitude: float, longitude: float, db: Session):
    db_user = models.Locations(
        latitude=latitude,
        longitude=longitude
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        'id': db_user.id,
        'latitude': latitude,
        'longitude': longitude
    }


def check_location(latitude: float, longitude: float, db: Session):
    result = db.execute(select(models.Locations).where(models.Locations.longitude == longitude)
                        .where(models.Locations.latitude == latitude)).first()
    return result[0]


def check_visited_point(animal_id: int, visited_id: int, db: Session):
    result = db.execute(select(models.VisitedLocations).where(models.VisitedLocations.id == visited_id).
                        where(models.VisitedLocations.animal_id == animal_id)).first()
    return result[0]


def get_visited_location(visited_id: int, db: Session):
    result = db.execute(select(models.VisitedLocations).where(models.VisitedLocations.id == visited_id)).first()
    return result[0]


def get_location(point_id: int, db: Session):
    result = db.execute(select(models.Locations).where(models.Locations.id == point_id)).first()
    return {
        'id': result[0].id,
        'latitude': result[0].latitude,
        'longitude': result[0].longitude
    }


def delete_visited_point(animalId: int, visitedPointId: int, db: Session):
    db.query(models.VisitedLocations).filter(models.VisitedLocations.id == visitedPointId).delete()
    db.commit()


def update_point_visit(animalId: int, visited_id: int, loc_id: int, db: Session):
    db.query(models.VisitedLocations).filter(models.VisitedLocations.id == visited_id).update(
        {
            models.VisitedLocations.loc_id: loc_id
        }
    )
    db.commit()
    s = get_visited_location(visited_id, db)
    return {
        'id': visited_id,
        'dateTimeOfVisitLocationPoint': s.date_of_visit,
        'locationPointId': loc_id
    }


def add_visit_point(animalId: int, pointId: int, db: Session):
    date = datetime.datetime.now()
    db_user = models.VisitedLocations(
        animal_id=animalId,
        date_of_visit=date,
        loc_id=pointId
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        'id': db_user.id,
        'dateTimeOfVisitLocationPoint': date,
        'locationPointId': pointId
    }


def last_visit_point(animalId: int, db: Session):
    result = db.execute(select(models.VisitedLocations).where(models.VisitedLocations.animal_id == animalId)).scalars().all()
    s = 0
    for res in result:
        s = res
    return s


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
