#calculate_weight.py
from pypfopt import EfficientFrontier, risk_models, expected_returns


def calculate_mu_sigma(data, tickers):
    precios={}
    for ticker in tickers:
        precios[ticker] = data[f'{ticker}'].values
    mu = expected_returns.mean_historical_return(precios, frequency=252, log_returns=True) #rentabilidades esperadas
    sigma = risk_models.sample_cov(precios) #matriz de covarianza y covarianzas
    return mu, sigma




def calculate_weight(mu, sigma):
    # Maximizando el ratio de Sharpe
    ef = EfficientFrontier(mu, sigma)

    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.portfolio_performance(verbose=True)

    return cleaned_weights 