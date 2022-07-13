"""
AmCAT4 Annotator Module API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from DigitalFootprintsBackend.api.apis import app_apis

app = FastAPI(
  title="DigitalFootprintsBackend",
  description=__doc__,
  openapi_tags=[
    dict(name="apis", description="Endpoints for accessing APIs and resources"),
  ]
)

app.include_router(app_apis)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
