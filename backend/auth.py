from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from config import settings

router = APIRouter()

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user: UserLogin, Authorize: AuthJWT = None):
    if user.email != settings.ADMIN_USER or user.password != settings.ADMIN_PASS:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = Authorize.create_access_token(subject=user.email)
    return JSONResponse(content={"access_token": access_token})
