import requests
from bs4 import BeautifulSoup
import csv
from typing import List
import os
import pandas as pd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/mensuales/resultados/PN00187MM/html"

def fetch_liquidez_table() -> List[List[str]]:
    """
    Extrae la tabla de liquidez en soles desde la web del BCRP y la retorna como lista de listas (filas y columnas).
    Cada fila de la tabla HTML será una fila en el CSV, y cada celda una columna.
    """
    resp = requests.get(URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    tablas = soup.find_all('table', class_=['series'])
    if not tablas:
        raise ValueError("No se encontró la tabla de liquidez en la página.")
    tabla_principal = tablas[0]
    datos = []
    for fila in tabla_principal.find_all('tr'):
        celdas = [celda.get_text(strip=True) for celda in fila.find_all(['th', 'td'])]
        if celdas:
            datos.append(celdas)
    return datos

def save_to_csv(data: List[List[str]], folder: str):
    """
    Guarda los datos extraídos en un archivo CSV en la carpeta indicada, con nombre datos_YYYY-MM-DD.csv.
    Solo guarda un nuevo archivo si la data es diferente a la última guardada en la carpeta.
    El CSV solo contiene la data original extraída de la web (sin columnas adicionales).
    """
    import glob
    from datetime import datetime

    fecha = os.path.basename(folder)
    filename = f"datos_{fecha}.csv"
    path = os.path.join(folder, filename)

    # Guardar temporalmente el scraping actual
    temp_path = path + '.tmp'
    with open(temp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

    # Buscar el último archivo CSV guardado en la carpeta (excluyendo el temporal)
    csv_files = sorted(glob.glob(os.path.join(folder, 'datos_*.csv')))
    last_csv = csv_files[-1] if csv_files else None

    # Comparar el archivo temporal con el último CSV guardado
    is_different = True
    if last_csv:
        with open(last_csv, 'r', encoding='utf-8') as f1, open(temp_path, 'r', encoding='utf-8') as f2:
            is_different = f1.read() != f2.read()

    if is_different:
        os.replace(temp_path, path)
    else:
        os.remove(temp_path)

