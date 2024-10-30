# main.py
import downloader
import analyse_data
import calculate_weight


def main():
    print(""" --- Informe de pesos óptimos del precio diario de acciones bursátiles --- 
          --- Incluye estadistica descriptiva---\n""")
    tickers = input("Ingrese los símbolos de los tickers separados por comas (ejemplo: MSFT, TSLA, NVDA): \n").split(",")
    tickers = [ticker.strip().upper() for ticker in tickers]  # Limpiar espacios y convertir a mayúsculas

    date_start = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    date_end = input("Ingrese la fecha de fin (YYYY-MM-DD): \n")
    print("\nDescargando datos...")
    data = downloader.downloader_data(tickers, date_start, date_end)
    print("Calculando rendimiento y otras métricas...")
    data = analyse_data.add_performance(data, tickers)

    fin = False

    while not fin:
        print("""\nMenú de opciones:
              1) Ver estadísticas descriptivas.
              2) Generar gráficos.
              3) Calcular péso optimo.
              4) Guardar informe en word y descargar.
              5) Salir\n """)
        opc = int(input("Ingresar opción:"))
        if opc == 1:
            print("Mostrando análisis descriptivo...")
            analyse_data.descriptive(data)
        elif opc == 2:
            print("""Escoja el tipo de gráfico que desea vizualizar:
                  1) Gráfico de series temporales.
                  2) Gráfico de cajas.\n""")
            opc = int(input("Elegir opción: "))
            if opc == 1:
                analyse_data.plot_line_series(data, tickers)
            elif opc == 2:
                analyse_data.plot_box_plot(data, tickers)
        elif opc == 3:
            mu, sigma = calculate_weight.calculate_mu_sigma(data, tickers)
            weights = calculate_weight.calculate_weight(mu, sigma)

            for ticker, weight in zip(tickers, weights):
                print(f"{ticker}: {weight:.2f}")



            


