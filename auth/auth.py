from fastapi.security import HTTPBasic
from passlib.context import CryptContext

from config import PASSWORD_SALT

security = HTTPBasic()

security_for_reg = HTTPBasic(auto_error=False)


hasher = CryptContext(schemes=['bcrypt'])


def encode_password(password):
    return hasher.hash(password + PASSWORD_SALT)


def verify_password(password, encoded_password):
    return hasher.verify(password + PASSWORD_SALT, encoded_password)