import schedule
import time
from scraper.scraper_dje import buscar_publicacoes
from database.models import salvar_publicacao, init_db

def executar():
    print("[INFO] Executando scraping agendado...")
    publicacoes = buscar_publicacoes()
    for pub in publicacoes:
        salvar_publicacao(pub)
        print(f"Salvo: {pub['numero_processo']}")

init_db()
schedule.every().day.at("08:00").do(executar)

while True:
    schedule.run_pending()
    time.sleep(60)
