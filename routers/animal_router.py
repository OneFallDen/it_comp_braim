from fastapi import routing, Depends
from sqlalchemy.orm import Session


from sql.db import get_db
from controllers.animal_controller import get_anim_info


router = routing.APIRouter()


@router.get('/animal/{animalId}', tags=['account'])
async def get_animal_info(animalId: int, db: Session = Depends(get_db)):
    return get_anim_info(animalId, db)
