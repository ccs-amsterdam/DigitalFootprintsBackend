import logging, datetime, random
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from DigitalFootprintsBackend.models import Project, PublicData
from DigitalFootprintsBackend import auth

#from amcat4annotator import schemas

def get_project_id(db: Session, name: str) -> int:
    project = db.query(Project.id).where(Project.name == name).first()
    if project is None:
        raise HTTPException(status_code=400, detail="Project doesn't exist")
    return project.id

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

def create_project(db: Session, name: str, password: str):
    p = db.query(Project).filter(Project.name == name).first()
    if p:
        logging.error(f"Project {name} already exists!")
        return None
    hpassword = auth.hash_password(password) if password else None
    db_project = Project(name=name, password=hpassword)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def set_publicdata(db: Session, project: str, submission_id: str, data: List[dict]):
    project_id = get_project_id(db, project)

    pd = db.query(PublicData).filter(PublicData.project == project_id, PublicData.submission_id == submission_id).first()

    timestamp = int(datetime.datetime.now().timestamp()*1000000)
    if pd is None:
        pd = PublicData(project=project_id, submission_id=submission_id, modified=timestamp, publicdata=data)
        db.add(pd)
    else:
        pd.modified = timestamp
        pd.publicdata = data
    db.commit()
    
def get_publicdata(db: Session, project: str, updated: Optional[int]): 
    project_id = get_project_id(db, project)

    lastupdate = db.query(func.max(PublicData.modified).label('modified')).where(PublicData.project == project_id).first()
    
    modified = lastupdate.modified if lastupdate is not None else None
    if updated is not None and modified is not None:
        if lastupdate.modified <= updated: 
            return {}, modified, False

    pd = db.query(PublicData).where(PublicData.project == project_id).all()
    data = [r.publicdata for r in pd]
    random.shuffle(data)
    return data, modified, True
 