from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from database.models import listar_publicacoes, atualizar_status_publicacao
from dotenv import load_dotenv
from pydantic import BaseModel  
import os

load_dotenv()

app = FastAPI()

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para ["http://localhost:3000"] em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Query

@app.get("/api/publicacoes")
def get_publicacoes(
    query: str = Query('', alias="query"),
    fromDate: str = Query('', alias="fromDate"),
    toDate: str = Query('', alias="toDate")
):
    return listar_publicacoes(query, fromDate, toDate)

class StatusUpdate(BaseModel):
    status: str

@app.patch("/api/publicacoes/{pub_id}")
def atualizar_status(pub_id: int, status_update: StatusUpdate):
    atualizado = atualizar_status_publicacao(pub_id, status_update.status)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    return {"message": "Status atualizado com sucesso"}


@app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    senha = data.get("password")

    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")

    if email == admin_user and senha == admin_pass:
        return {
            "token": "fake-jwt-token",
            "user": {
                "email": admin_user,
                "name": "Admin",
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
