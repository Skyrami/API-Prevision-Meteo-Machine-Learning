import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from api import Authentification

from datascience.loader import UserData
from datascience.classifier import DataClassifier
from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod

router = APIRouter(
    dependencies=[Depends(Authentification.get_authentification_header)],
    prefix="/datascientest/rainproject/classifier",
    tags=["classifier"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/{classifier_id}/predict",
    name="Get prediction from your data",
    responses={200: {"description": "Will it rain tomorrow ? Or not ?"}},
)
async def predict(
    user_data: UserData,
    classifier_id: ClassifierId,
    data_mode: Optional[DataMode] = DataMode.full,
    scaling_method: Optional[ScalingMethod] = ScalingMethod.standard,
    sampling_method: Optional[SamplingMethod] = SamplingMethod.none,
):
    cls = DataClassifier(classifier_id, data_mode, scaling_method, sampling_method)
    cls.load()
    result = cls.predict(user_data.getAsDataFrame())[0]
    if result == 1:
        return {"RainTomorrow": "Yes"}
    else:
        return {"RainTomorrow": "No"}
