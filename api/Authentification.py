from fastapi import Header, HTTPException, Request
from fastapi import APIRouter, Depends


users_db = [
    {
        # alice:wonderland
        'id': 'YWxpY2U6d29uZGVybGFuZA==',
    },
    {
        # bob:builder
        'id': 'Ym9iOmJ1aWxkZXI=',
    },
    {
        # clementine:mandarine
        'id': 'Y2xlbWVudGluZTptYW5kYXJpbmU=',
    },
]

router = APIRouter(
    prefix="/datascientest/rainproject/classifier",
    tags=["classifier"],
    responses={404: {"description": "Not found"}},
)


async def get_authentification_header(
    request: Request, auth_token: str = Header("authentification")
):
    credentials = str(auth_token)
    # vérification dans la base de données
    for user in users_db:
        if (credentials == user['id']):
            return "Vous êtes autorisé à utiliser l'API"
    raise Exception("Forbidden acces: Votre mot de passe est incorrect", 403)

