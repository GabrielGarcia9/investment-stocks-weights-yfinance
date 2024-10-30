# calculate_weight.py
from pypfopt import EfficientFrontier, risk_models, expected_returns
import pandas as pd

def calculate_mu_sigma(data, tickers):
    precios = pd.DataFrame({ticker: data[f'{ticker}'].values for ticker in tickers}, index=data.index)
    
    mu = expected_returns.mean_historical_return(precios, frequency=252, log_returns=True)  # Rentabilidades esperadas
    sigma = risk_models.sample_cov(precios)  # Matriz de covarianza
    return mu, sigma

def calculate_weight(mu, sigma):
    # Maximizando el ratio de Sharpe
    ef = EfficientFrontier(mu, sigma)

    weights = ef.max_sharpe() # Calcula los pesos asignando a una variable que no es necesaria directamente
    cleaned_weights = ef.clean_weights()
    
    ef.portfolio_performance(verbose=True)

    return cleaned_weights
