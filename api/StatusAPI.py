from fastapi import APIRouter, HTTPException

from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod
from datascience.classifier import DataClassifier

router = APIRouter(
    prefix="/datascientest/rainproject",
    tags=["status"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ping")
async def ping():
    return 1


@router.get("/healthcheck")
async def healthcheck():
    for clsId in ClassifierId:
        for dataMode in DataMode:
            for scalingMethod in ScalingMethod:
                for samplingMethod in SamplingMethod:
                    classifier = DataClassifier(
                        clsId, dataMode, scalingMethod, samplingMethod
                    )
                    classifier.load()
                    if not classifier.loaded:
                        print("{} is not Ready".format(classifier.name))
                        raise HTTPException(
                            status_code=503, detail="Some classifier are not available"
                        )
    return 1
