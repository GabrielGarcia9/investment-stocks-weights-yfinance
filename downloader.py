#downloader.py
import yfinance as yf



# Obtener datos históricos de los activos de Yahoo Finance
def downloader_data(tickers: list, date_start: str, date_end: str):
    return yf.download(tickers, start = date_start, end = date_end)["Adj Close"].dropna()


