import logging
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from DigitalFootprintsBackend.models import Project
from DigitalFootprintsBackend import auth
#from amcat4annotator import schemas


def verify_password(db: Session, project: str, password: str):
    p = db.query(Project).filter(Project.name == project).first()
    if not p:
        logging.warning(f"Project {p} does not exist")
        return None
    elif not p.password:
        logging.warning(f"Password for {p} is missing")
        return None
    elif not auth.verify_password(password, p.password):
        logging.warning(f"Password for {p} did not match")
        return None
    else:
        return u

