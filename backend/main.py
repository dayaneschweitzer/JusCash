from scraper.scraper_dje import buscar_publicacoes
from database.models import init_db, salvar_publicacao
from auth import router as auth_router

app.include_router(auth_router)

init_db()  

if __name__ == "__main__":
    publicacoes = buscar_publicacoes()
    print(f"{len(publicacoes)} publicações encontradas.")

    for pub in publicacoes:
        salvar_publicacao(pub)
        print(f"Publicação salva: {pub['numero_processo']}")
