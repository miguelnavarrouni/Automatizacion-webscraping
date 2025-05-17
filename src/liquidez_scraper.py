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
        if celdas:  # Solo filas no vacías
            datos.append(celdas)
    return datos

def save_to_csv(data: List[List[str]], path: str):
    """
    Guarda los datos extraídos en un archivo CSV en la ruta indicada.
    Si el archivo ya existe, concatena los datos nuevos y antiguos y elimina duplicados por la columna de fecha.
    Además, agrega una columna 'data-liquidez-fecha' con la fecha de la carpeta.
    """
    # Extraer la fecha de la ruta (asume formato .../AAAA-MM-DD/datos.csv)
    fecha = os.path.basename(os.path.dirname(path))
    # Añadir la columna de fecha a cada fila de datos (excepto encabezado si existe)
    data_con_fecha = []
    for i, fila in enumerate(data):
        if i == 0 and (fila[0].lower().startswith('fecha') or fila[0].lower().startswith('ene')):
            # Encabezado
            data_con_fecha.append(fila + ['data-liquidez-fecha'])
        else:
            data_con_fecha.append(fila + [fecha])
    # Guardar temporalmente el scraping
    temp_path = path + '.tmp'
    with open(temp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data_con_fecha)
    # Limpiar duplicados si ya existe el archivo final
    df_new = pd.read_csv(temp_path, header=None)
    if os.path.exists(path):
        df_old = pd.read_csv(path, header=None)
        df = pd.concat([df_old, df_new], ignore_index=True)
        df = df.drop_duplicates(subset=[0])
    else:
        df = df_new
    df.to_csv(path, index=False, header=False)
    os.remove(temp_path)

