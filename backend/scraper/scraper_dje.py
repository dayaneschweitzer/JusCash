from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import time

CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')

def iniciar_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def buscar_publicacoes():
    driver = iniciar_navegador()
    wait = WebDriverWait(driver, 20)
    publicacoes = []

    try:
        print("[INFO] Acessando página inicial do DJE...")
        driver.get("https://dje.tjsp.jus.br/cdje/index.do")

        print("[INFO] Clicando no link 'Pesquisa Avançada'...")
        link_pesquisa = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Pesquisa Avançada")))
        link_pesquisa.click()

        # Aguarda redirecionamento para o formulário de pesquisa
        wait.until(EC.presence_of_element_located((By.ID, "dtInicioString")))

        # Preenche data
        hoje = datetime.now().strftime("%d/%m/%Y")
        driver.execute_script("document.getElementById('dtInicioString').removeAttribute('readonly')")
        driver.execute_script("document.getElementById('dtFimString').removeAttribute('readonly')")
        driver.find_element(By.ID, "dtInicioString").clear()
        driver.find_element(By.ID, "dtInicioString").send_keys(hoje)
        driver.find_element(By.ID, "dtFimString").clear()
        driver.find_element(By.ID, "dtFimString").send_keys(hoje)

        # Seleciona o Caderno 3 - Judicial - 1ª Instância - Capital - Parte I
        select_caderno = Select(driver.find_element(By.ID, "cadernos"))
        select_caderno.select_by_visible_text("caderno 3 - Judicial - 1ª Instância - Capital - Parte I")

        # Preenche palavras-chave
        palavras = driver.find_element(By.ID, "procura")
        palavras.clear()
        palavras.send_keys('RPV "pagamento pelo INSS"')

        # Clica em Pesquisar
        driver.find_element(By.XPATH, '//input[@type="submit" and @value="Pesquisar"]').click()

        print("[INFO] Aguardando resultados...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "resultado")))

        links = driver.find_elements(By.XPATH, '//a[contains(@href, "consultaSimples.do")]')
        print(f"[INFO] {len(links)} links de publicação encontrados.")

        for i, link in enumerate(links):
            href = link.get_attribute("href")
            driver.execute_script("window.open(arguments[0]);", href)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            texto = soup.get_text(separator=" ", strip=True)

            publicacoes.append({
                "numero_processo": extrair_processo(texto),
                "data_disponibilizacao": hoje,
                "autores": extrair_autores(texto),
                "advogados": extrair_advogados(texto),
                "conteudo": texto,
                "valor_bruto": extrair_valor(texto),
                "valor_juros": extrair_juros(texto),
                "honorarios": extrair_honorarios(texto)
            })

            print(f"[{i + 1}] Publicação capturada.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        driver.quit()

    return publicacoes

# Funções auxiliares de extração
def extrair_processo(texto):
    match = re.search(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto)
    return match.group(0) if match else ""

def extrair_autores(texto):
    match = re.search(r"Autor(?:es)?[:\-]?\s*(.*?)\s+(ADV|Réu|Processo|RÉU|REQUERIDO)", texto, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extrair_advogados(texto):
    match = re.search(r"ADV(?:OGADO)?(?:\(A\))?:?\s*(.*?)\s{2,}", texto, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extrair_valor(texto):
    match = re.search(r"R\$ ?[\d\.\,]+", texto)
    return match.group(0) if match else ""

def extrair_juros(texto):
    match = re.search(r"juros morat[óo]rios.*?R\$ ?[\d\.\,]+", texto, re.IGNORECASE)
    return match.group(0).split('R$')[-1].strip() if match else ""

def extrair_honorarios(texto):
    match = re.search(r"honor[áa]rios(?: advocat[íi]cios)?[:\-]?\s*R\$ ?[\d\.\,]+", texto, re.IGNORECASE)
    return match.group(0).split('R$')[-1].strip() if match else ""
