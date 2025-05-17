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

def fetch_liquidez_table() -> pd.DataFrame:
    """
    Extrae la tabla de liquidez en soles desde la web del BCRP y la retorna como DataFrame de dos columnas: Fecha, Liquidez.
    """
    resp = requests.get(URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    tabla = soup.find('table', class_='series')
    if not tabla:
        raise ValueError("No se encontró la tabla de liquidez en la página.")
    filas = tabla.find_all('tr')
    fechas = []
    valores = []
    for fila in filas[1:]:  # saltar encabezado
        celdas = fila.find_all('td')
        if len(celdas) == 2:
            fechas.append(celdas[0].get_text(strip=True))
            valores.append(celdas[1].get_text(strip=True))
    df = pd.DataFrame({"Fecha": fechas, "Liquidez": valores})
    df = df.drop_duplicates()
    return df

def save_to_csv(data: pd.DataFrame, folder: str):
    """
    Guarda el DataFrame en un archivo CSV en la carpeta indicada, con nombre datos_YYYY-MM-DD.csv.
    Solo guarda un nuevo archivo si la data es diferente a la última guardada en la carpeta.
    """
    import glob
    fecha = os.path.basename(folder)
    filename = f"datos_{fecha}.csv"
    path = os.path.join(folder, filename)
    temp_path = path + '.tmp'
    data.to_csv(temp_path, index=False)
    csv_files = sorted(glob.glob(os.path.join(folder, 'datos_*.csv')))
    last_csv = csv_files[-1] if csv_files else None
    is_different = True
    if last_csv:
        with open(last_csv, 'r', encoding='utf-8') as f1, open(temp_path, 'r', encoding='utf-8') as f2:
            is_different = f1.read() != f2.read()
    if is_different:
        os.replace(temp_path, path)
    else:
        os.remove(temp_path)

