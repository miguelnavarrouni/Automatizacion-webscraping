import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.cpi_api import fetch_cpi_mexico
from src.liquidez_scraper import save_to_csv

fecha = os.environ['FECHA']
os.makedirs(f'data/cpi/{fecha}', exist_ok=True)

datos = fetch_cpi_mexico()
save_to_csv(datos, f'data/cpi/{fecha}', tipo='CPI')
