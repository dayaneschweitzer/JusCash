from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from database.models import (
    listar_publicacoes,
    listar_publicacoes_novas,
    atualizar_status_publicacao,
    registrar_usuario
)
from dotenv import load_dotenv
from pydantic import BaseModel
from scraper.scraper_dje import executar_scraper
from datetime import datetime
import os

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/publicacoes")
def get_publicacoes(
    query: str = Query('', alias="query"),
    fromDate: str = Query('', alias="fromDate"),
    toDate: str = Query('', alias="toDate")
):
    return listar_publicacoes(query, fromDate, toDate)

@app.get("/api/publicacoes/novas")
def get_publicacoes_novas(
    fromDate: str = Query('', alias="fromDate"),
    toDate: str = Query('', alias="toDate")
):
    return listar_publicacoes_novas(fromDate, toDate)

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

@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    nome = data.get("name")
    email = data.get("email")
    senha = data.get("password")

    if not nome or not email or not senha:
        raise HTTPException(status_code=400, detail="Dados incompletos")

    try:
        user = registrar_usuario(nome, email, senha)
        return {
            "message": "Usuário registrado com sucesso",
            "user": user
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

class ScraperRequest(BaseModel):
    from_date: str
    to_date: str

@app.post("/api/scraper-dje")
def iniciar_scraper(request: ScraperRequest):
    try:
        from_date = datetime.fromisoformat(request.from_date.replace("Z", "")).strftime("%d/%m/%Y")
        to_date = datetime.fromisoformat(request.to_date.replace("Z", "")).strftime("%d/%m/%Y")

        executar_scraper(from_date, to_date)
        return {"message": "Scraper executado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

