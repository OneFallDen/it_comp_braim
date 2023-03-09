from sqlalchemy import select
from sqlalchemy.orm import Session

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
