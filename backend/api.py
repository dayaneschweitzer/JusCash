from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from database.models import listar_publicacoes, atualizar_status_publicacao
from dotenv import load_dotenv
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

@app.get("/api/publicacoes")
def get_publicacoes(
    query: str = "",
    fromDate: str = "",
    toDate: str = ""
):
    return listar_publicacoes(query=query, fromDate=fromDate, toDate=toDate)

@app.patch("/api/publicacoes/{pub_id}")
def atualizar_status(pub_id: int, status: str = Body(...)):
    atualizado = atualizar_status_publicacao(pub_id, status)
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
