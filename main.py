import downloader
import analyse_data 
import calculate_weight


date_start = "2023-01-16"
date_end="2024-09-30"
tickers = ["MSFT", "TSLA",'NVDA', 'AAPL','GOOG','AMZN', 'AMD','SBUX']


data = downloader.downloader_data(tickers, date_start, date_end)
data = analyse_data.add_performance(data, tickers)
analyse_data.descriptive(data)
analyse_data.plot_line_series(data, tickers)
analyse_data.plot_box_plot(data, tickers)
mu, sigma = calculate_weight.calculate_mu_sigma(data, tickers)
print(calculate_weight.calculate_weight(mu, sigma))