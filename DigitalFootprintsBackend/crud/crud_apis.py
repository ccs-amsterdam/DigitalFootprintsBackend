import logging
import requests
from sqlalchemy import true

from sqlalchemy.orm import Session

from DigitalFootprintsBackend.models import Transformer

from typing import List

from fastapi import HTTPException


def tiktok_video_details(db: Session, ids: List[int]) -> List[dict]:
    details = []
    for id in ids:
        try:
            ## the username appears in the url after a few redirects.
            ## this way we don't have to scrape the body
            url = "https://www.tiktokv.com/share/video/{id}/".format(id=id)
            for attempt in range(0,5):
                res = requests.head(url)
                url = res.headers['Location']
                if '@' in url:
                    user = url.split('@')[1].split('/')[0]
                    details.append({"id": id, "user": user})
                    break        
        except Exception as e:
            logging.error(e)
            details.append({"id": id, "user": ""})
    return details
