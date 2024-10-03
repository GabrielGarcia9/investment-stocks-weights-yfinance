from seaborn import lineplot, boxplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Calcular rendimientos diarios

def add_performance(data, tickers):

    for ticker in tickers:
        data[f'R{ticker}'] = np.log(data[ticker] / data[ticker].shift(1))

    return data.dropna()

def descriptive(data):
    return data.describe().round(2).T

def plot_line_series(data, tickers):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for ticker in tickers: # Graficar los precios históricos de JNJ, MSFT, NVDA y TSLA en un solo gráfico
        lineplot(data=data, x='Date', y=ticker, label=f'adj close {ticker}')
        
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Historical Stock Prices')
    plt.xticks(rotation=45)

    # Agregar líneas verticales para cada año
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    for year in years:
        year_data = data[data.index.year == year] # Filtrar los datos por el año actual
        if len(year_data) > 0:
            # Dibujar una línea vertical en el primer día del año
            plt.axvline(year_data.index[0], linestyle='--', color='gray', linewidth=0.2)
            
    # Agregar líneas horizontales en incrementos de 50 para los precios
    price_levels = range(0, int(data[ticker].max()), 50)

    for level in price_levels:
        plt.axhline(level, linestyle='--', color='gray', linewidth=0.2)
        
    plt.legend(loc='upper left')
    plt.show()

def plot_box_plot(data, tickers):

    retornos = {}
    for ticker in tickers:
        retornos[f'R{ticker}'] = data[f'R{ticker}'].values

    plt.figure(figsize=(15, 5))

    boxplot(data=pd.DataFrame(retornos))
    plt.title('Boxplot Analysis of Assets Returns')

    plt.show()