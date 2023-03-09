from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_account


def get_acc_info(account_id: int, db: Session):
    if not account_id:
        raise HTTPException(status_code=400)
    if account_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_account(account_id, db)
    except:
        raise HTTPException(status_code=404)
