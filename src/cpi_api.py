import os
import pandas as pd
import tradingeconomics as te

def fetch_cpi_mexico(init_date: str = '2015-01-01') -> pd.DataFrame:
    """
    Descarga el índice de precios al consumidor (CPI) de México usando el paquete oficial de Trading Economics.
    Retorna un DataFrame con columnas: Fecha, CPI.
    """
    # Login usando variable de entorno 'apikey' si existe
    if 'apikey' in os.environ:
        te.login()
    else:
        te.login('')
    data = te.getHistoricalData(country='Mexico', indicator='Consumer Price Index CPI', initDate=init_date)
    df = pd.DataFrame(data)
    # Normalizar nombres de columnas
    if 'DateTime' in df.columns:
        df = df.rename(columns={'DateTime': 'Fecha', 'Value': 'CPI'})
        df = df[['Fecha', 'CPI']]
    elif 'date' in df.columns:
        df = df.rename(columns={'date': 'Fecha', 'value': 'CPI'})
        df = df[['Fecha', 'CPI']]
    else:
        df = df.iloc[:, :2]
    df = df.drop_duplicates()
    return df

# Puedes reutilizar save_to_csv de liquidez_scraper para guardar el DataFrame
