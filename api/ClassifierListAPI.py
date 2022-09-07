from fastapi import APIRouter, Depends, HTTPException
from api import Authentification
from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod
from datascience import definition

router = APIRouter(
    dependencies=[Depends(Authentification.get_authentification_header)],
    prefix="/datascientest/rainproject/classifier",
    tags=["classifier"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list():
  
    print("Les Classifiers disponibles : \n")
    resultat_cls = []
    for clsId in ClassifierId:
        def_ClassifierId = definition.getClassifierIdDescription(clsId)
        info_cls = [{clsId : def_ClassifierId}]
        resultat_cls = resultat_cls.__add__(info_cls)
        print("{} : {}".format(clsId,def_ClassifierId))
    print("\n")
      
    print("Les DataMode disponibles : \n")  
    resultat_dtmd = []
    for dataMode in DataMode:
        def_dataMode = definition.getDataModeDescription(dataMode)
        info_dtmd = [{DataMode : def_dataMode}]
        resultat_dtmd = resultat_dtmd.__add__(info_dtmd) 
        print("{} : {}".format(dataMode,def_dataMode))
    print("\n")
    
    print("Les ScalingMethod disponibles : \n")
    resultat_scmd = []
    for scalingMethod in ScalingMethod:
        def_scalingMethod = definition.getScalingMethodDescription(scalingMethod)
        info_scmd = [{scalingMethod : def_scalingMethod}]
        resultat_scmd = resultat_scmd.__add__(info_scmd) 
        print("{} : {}".format(scalingMethod,def_scalingMethod)) 
    print("\n") 
    
    print("Les SamplingMethod disponibles : \n")
    resultat_samd = []  
    for samplingMethod in SamplingMethod:
        def_samplingMethod = definition.getSamplingMethodDescription(samplingMethod)
        info_samd = [{samplingMethod : def_samplingMethod}]
        resultat_samd = resultat_samd.__add__(info_samd) 
        print("{} : {}".format(samplingMethod,def_samplingMethod))  
    print("\n") 

    resultat_list = []

    resultat_list = resultat_cls + resultat_dtmd + resultat_scmd + resultat_samd

    return "{}".format(resultat_list)
