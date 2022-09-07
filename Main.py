from fastapi import Depends, FastAPI

from api import (
    ClassifierInfoScoringAPI,
    StatusAPI,
    ClassifierListAPI,
    ClassifierPredictAPI,
)

api = FastAPI()

api.include_router(StatusAPI.router)
api.include_router(ClassifierInfoScoringAPI.router)
api.include_router(ClassifierListAPI.router)
api.include_router(ClassifierPredictAPI.router)
