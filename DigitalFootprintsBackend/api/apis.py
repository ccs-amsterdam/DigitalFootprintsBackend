from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from DigitalFootprintsBackend import models
from DigitalFootprintsBackend.crud import crud_apis
from DigitalFootprintsBackend.database import engine, get_db
from DigitalFootprintsBackend.models import TiktokVideo

models.Base.metadata.create_all(bind=engine)
app_apis = APIRouter(prefix="/apis", tags=["apis"])



@app_apis.post("/tiktokvideos", status_code=200)
def get_tiktok_video_details(ids: list = Body(None, description='TikTok video ids'), 
                             db: Session = Depends(get_db)):
    """
    Given a list of tiktok video ids, return video details
    """
    return crud_apis.tiktok_video_details(db, ids)
