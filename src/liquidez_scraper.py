import requests
from bs4 import BeautifulSoup
import csv
from typing import List

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/mensuales/resultados/PN00187MM/html"

def fetch_liquidez_table() -> List[List[str]]:
    """
    Extrae la tabla de liquidez en soles desde la web del BCRP y la retorna como lista de listas (filas).
    No guarda el archivo, solo retorna los datos.
    """
    resp = requests.get(URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    tablas = soup.find_all('table', class_=['series'])
    if not tablas:
        raise ValueError("No se encontró la tabla de liquidez en la página.")
    tabla_principal = tablas[0]
    filas = tabla_principal.find_all('tr')
    datos = []
    for fila in filas:
        celdas = [celda.get_text(strip=True) for celda in fila.find_all(['th', 'td'])]
        datos.append(celdas)
    return datos

def save_to_csv(data: List[List[str]], path: str):
    """
    Guarda los datos extraídos en un archivo CSV en la ruta indicada.
    """
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

