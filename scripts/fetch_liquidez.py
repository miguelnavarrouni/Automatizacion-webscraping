import os
from src.liquidez_scraper import fetch_liquidez_table, save_to_csv

fecha = os.environ['FECHA']
os.makedirs(f'data/liquidez/{fecha}', exist_ok=True)
datos = fetch_liquidez_table()
save_to_csv(datos, f'data/liquidez/{fecha}/datos.csv')
