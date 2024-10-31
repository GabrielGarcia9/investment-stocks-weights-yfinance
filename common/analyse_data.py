from seaborn import set, lineplot, boxplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def add_performance(data, tickers):
    for ticker in tickers:
        data[f'R{ticker}'] = np.log(data[ticker] / data[ticker].shift(1))
    return data.dropna()

def descriptive(data):
    return data.describe().round(2).T

def plot_line_series(data, tickers):
    set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for ticker in tickers:
        lineplot(data=data, x=data.index, y=ticker, label=ticker)
    plt.xlabel('Fecha')
    plt.ylabel('Precio Ajustado')
    plt.title('Precios Históricos de las Acciones')
    plt.legend()
    plt.xticks(rotation=45)

def show_plot_line_series(data, tickers):
    plot_line_series(data, tickers)
    plt.show()

def plot_box_plot(data, tickers):
    set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    boxplot(data=data[[f'R{ticker}' for ticker in tickers]])
    plt.title('Análisis de Box Plot de Retornos')
    plt.ylabel('Retorno')

def show_plot_box_plot(data, tickers):
    plot_box_plot(data, tickers)
    plt.show()
