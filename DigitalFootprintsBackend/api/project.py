from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List


from DigitalFootprintsBackend import models
from DigitalFootprintsBackend.crud import crud_project
from DigitalFootprintsBackend.database import engine, get_db
from DigitalFootprintsBackend.models import Project

from DigitalFootprintsBackend.auth import auth_project, get_token


models.Base.metadata.create_all(bind=engine)

app_project = APIRouter(prefix="/project", tags=["project"])


@app_project.post("/this/token", status_code=200)
def get_my_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Get a token via password login
    """
    project = crud_project.verify_password(
        db, project=form_data.project, password=form_data.password)
    if not project:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect projectname or password")
    return {"token": get_token(project)}


@app_project.get("/this/token")
def verify_my_token(project: Project = Depends(auth_project)):
    """
    Verify a token, and get basic project information
    """
    return {"token": get_token(project),
            "name": project.name}


@app_project.post("/this/password", status_code=204)
def set_password(password: str = Body(None, description="The new password"),
                 project: Project = Depends(auth_project),
                 db: Session = Depends(get_db)):
    """
    Set a new password. 
    """

    if not password:
        raise HTTPException(status_code=400, detail={
                            "error": "Body needs to have password"})

    crud_project.change_password(db, project.name, password)
    return Response(status_code=204)

@app_project.get("/{project}")
def get_project(project: str):
    """
    get project settings
    """
    return {"hey": "hi!",
            "name": project}

@app_project.post("/{project}/publicdata", status_code=204)
def set_publicdata(project: str,
                   submission_id: str = Body(None, description='the submission id'),
                   data: dict = Body({}, description='A list of dictionaries with the keys "item" and "score"'),
                   db: Session = Depends(get_db)):
    
    crud_project.set_publicdata(db, project, submission_id, data)
    # try:
    # except Exception :
    #     db.rollback()
    #     return Response(status_code=400)

@app_project.get("/{project}/publicdata", status_code=200)
def get_publicdata(project: str,
                   db: Session = Depends(get_db)): 
    data = crud_project.get_publicdata(db, project, 0)
    print(data)
    return(data)
