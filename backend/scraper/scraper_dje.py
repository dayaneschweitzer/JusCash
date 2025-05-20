import time
import sqlite3
import re
import traceback
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database/publicacoes.db')

def init_browser():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def salvar_publicacao(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO publicacoes (
            numero_processo, autores, reu, advogados, valor_bruto,
            valor_juros, honorarios, conteudo, status, data_publicacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['numero_processo'],
        data['autores'],
        "Instituto Nacional do Seguro Social - INSS",
        data['advogados'],
        data['valor_bruto'],
        data['valor_juros'],
        data['honorarios'],
        data['conteudo'],
        "novas",
        data['data_publicacao']
    ))
    conn.commit()
    conn.close()

def extrair_dados_da_publicacao(html_element, data_publicacao):
    texto = html_element.text

    numero_processo = ""
    match_proc = re.search(r"\b\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}\b", texto)
    if match_proc:
        numero_processo = match_proc.group().strip()

    advogados = ""
    match_adv = re.search(r"ADV.*?:\s*([^\n]*)", texto)
    if match_adv:
        advogados = match_adv.group(1).strip()

    autores = ""
    match_autor = re.search(r"Autor(?:\(es\))?:\s*(.+)", texto)
    if match_autor:
        autores = match_autor.group(1).strip()

    valor_bruto = ""
    match_bruto = re.search(r"(?i)valor(?:\sprincipal)?(?:\sbruto)?[:\s]*R\$\s*([\d\.,]+)", texto)
    if match_bruto:
        valor_bruto = match_bruto.group(1).strip()

    valor_juros = ""
    match_juros = re.search(r"(?i)juros(?:\smoratórios)?[:\s]*R\$\s*([\d\.,]+)", texto)
    if match_juros:
        valor_juros = match_juros.group(1).strip()

    honorarios = ""
    match_hon = re.search(r"(?i)honor[aá]rios(?:\sadvocat[ií]cios)?[:\s]*R\$\s*([\d\.,]+)", texto)
    if match_hon:
        honorarios = match_hon.group(1).strip()

    return {
        "numero_processo": numero_processo,
        "autores": autores,
        "advogados": advogados,
        "valor_bruto": valor_bruto,
        "valor_juros": valor_juros,
        "honorarios": honorarios,
        "conteudo": texto,
        "data_publicacao": data_publicacao
    }

def executar_scraper(from_date: str, to_date: str):
    print(f"Iniciando scraper com data de {from_date} até {to_date}")
    driver = init_browser()
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://dje.tjsp.jus.br/cdje/consultaAvancada.do#buscaavancada")
        print("Página carregada")

        wait.until(EC.element_to_be_clickable((By.ID, "cadernos")))
        print("Campo cdCaderno disponível")

        wait.until(EC.presence_of_element_located((By.NAME, "dadosConsulta.dtInicio")))
        driver.execute_script("document.getElementsByName('dadosConsulta.dtInicio')[0].removeAttribute('readonly');")
        dt_inicio = driver.find_element(By.NAME, "dadosConsulta.dtInicio")
        dt_inicio.clear()
        dt_inicio.send_keys(from_date)

        wait.until(EC.presence_of_element_located((By.NAME, "dadosConsulta.dtFim")))
        driver.execute_script("document.getElementsByName('dadosConsulta.dtFim')[0].removeAttribute('readonly');")
        dt_fim = driver.find_element(By.NAME, "dadosConsulta.dtFim")
        dt_fim.clear()
        dt_fim.send_keys(to_date)
        print("Datas preenchidas")

        wait.until(EC.presence_of_element_located((By.NAME, "dadosConsulta.cdCaderno")))
        caderno = driver.find_element(By.NAME, "dadosConsulta.cdCaderno")
        for option in caderno.find_elements(By.TAG_NAME, "option"):
            if "Caderno 3 - Judicial - 1ª Instância - Capital - Parte I" in option.text:
                option.click()
                print("Caderno selecionado")
                break

        wait.until(EC.presence_of_element_located((By.NAME, "dadosConsulta.pesquisaLivre")))
        palavra_chave = driver.find_element(By.NAME, "dadosConsulta.pesquisaLivre")
        palavra_chave.clear()
        palavra_chave.send_keys('"RPV" e "Pagamento pelo INSS"')
        print("Palavras-chave preenchidas")

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Pesquisar']")))
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Pesquisar']").click()
        print("Clique em pesquisar")

        time.sleep(5)

        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@colspan='2' and @align='left']")))
        publicacoes = driver.find_elements(By.XPATH, "//td[@colspan='2' and @align='left']")
        print(f"{len(publicacoes)} publicações encontradas")

        for publicacao in publicacoes:
            print("Extraindo uma publicação...")
            dados = extrair_dados_da_publicacao(publicacao, from_date)
            print("Publicação extraída:", dados)
            salvar_publicacao(dados)

        print("Todas as publicações foram salvas no banco com sucesso.")

    except Exception as e:
        print(f"[ERRO NO SCRAPER] {e}")
        traceback.print_exc()
        driver.save_screenshot("erro_scraper.png")
        raise
    finally:
        driver.quit()
