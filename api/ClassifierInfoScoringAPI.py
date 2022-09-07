from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datascience.classifier import DataClassifier
from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod
from api import Authentification


router = APIRouter(
    dependencies=[Depends(Authentification.get_authentification_header)],
    prefix="/datascientest/rainproject/classifier",
    tags=["classifier"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{classifier_id}",
    name="Get info from the classifier you chose",
)
async def getInfo(
    classifier_id: ClassifierId,
    data_mode: Optional[DataMode] = DataMode.full,
    scaling_method: Optional[ScalingMethod] = ScalingMethod.standard,
    sampling_method: Optional[SamplingMethod] = SamplingMethod.none,
):
    cls = DataClassifier(classifier_id, data_mode, scaling_method, sampling_method)
    cls.load()
    info = cls.stats
    return "{} = {}".format(cls.name, info)
