from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from database.models import listar_publicacoes, atualizar_status_publicacao, registrar_usuario
from dotenv import load_dotenv
from pydantic import BaseModel
import os

# Carrega variáveis de ambiente
load_dotenv()

# ✅ Instância única do app FastAPI
app = FastAPI()

# ✅ Middleware CORS corretamente configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] durante desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ GET /api/publicacoes
@app.get("/api/publicacoes")
def get_publicacoes(
    query: str = Query('', alias="query"),
    fromDate: str = Query('', alias="fromDate"),
    toDate: str = Query('', alias="toDate")
):
    return listar_publicacoes(query, fromDate, toDate)

# ✅ PATCH /api/publicacoes/{id}
class StatusUpdate(BaseModel):
    status: str

@app.patch("/api/publicacoes/{pub_id}")
def atualizar_status(pub_id: int, status_update: StatusUpdate):
    atualizado = atualizar_status_publicacao(pub_id, status_update.status)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    return {"message": "Status atualizado com sucesso"}

# ✅ POST /api/login
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

# ✅ POST /api/register
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
