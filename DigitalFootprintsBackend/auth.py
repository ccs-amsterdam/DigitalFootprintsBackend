import json
import logging
from typing import Optional

from authlib.jose import JsonWebSignature
import bcrypt
from authlib.jose.errors import DecodeError

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer


from sqlalchemy.orm import Session

from DigitalFootprintsBackend.models import Project
from DigitalFootprintsBackend.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/project/this/token")

SECRET_KEY = "Enter very secret key here"


async def auth_project(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Project:
    project = verify_token(db, token)
    if not project:
        raise HTTPException(status_code=400, detail="Invalid token")
    return project


def _get_token(payload: dict) -> str:
    return JsonWebSignature().serialize_compact(
        protected={'alg': 'HS256'},
        payload=json.dumps(payload).encode('utf-8'),
        key=SECRET_KEY).decode("ascii")


def get_token(project: Project) -> str:
    t = _get_token(payload={'project': project.name})
    if not t:
        logging.warning('Could not create token')
        return None
    return t


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, db_password: str):  
    return bcrypt.checkpw(password.encode("utf-8"), db_password.encode("utf-8"))


def _verify_token(token: str) -> Optional[dict]:
    try:
        payload = JsonWebSignature().deserialize_compact(token, SECRET_KEY)
    except DecodeError:
        return None
    return json.loads(payload['payload'].decode("utf-8"))


def verify_token(db: Session, token: str = Depends(oauth2_scheme)) -> Optional[Project]:
    """
    Verify the given token, returning the authenticated Project

    If the token is invalid, expired, or the project does not exist, returns None
    """
    payload = _verify_token(token)
    if payload is None or 'project' not in payload:
        logging.warning("Invalid payload")
        return None
    u = db.query(Project).filter(Project.name == payload['project']).first()
    if not u:
        logging.warning("project does not exist")
        return None
    return u







