# main.py
import downloader
import analyse_data
import calculate_weight
from to_generate_word import generar_informe
from to_generate_excel import generar_excel
from prettytable.colortable import ColorTable, Themes
import pandas as pd

def print_table(df, theme=Themes.OCEAN):
    table = ColorTable(theme=theme)
    table.field_names = df.columns.tolist()
    table.add_rows(df.values.tolist())
    print(table)

# main.py (parte donde descargas los datos)
def main():
    # Introducción y descripción de variables financieras
    print("""
    --- Bienvenido al Informe de Análisis de Inversión ---
    
    Este programa permite realizar un análisis de acciones bursátiles mediante los siguientes conceptos:
    
    1) Rendimiento Diario: Cambio porcentual diario en el precio de las acciones, indicando la ganancia o pérdida relativa.
    2) Volatilidad: Mide la variabilidad del precio de las acciones a lo largo del tiempo.
    3) Peso Óptimo: Distribución óptima de la inversión en las acciones seleccionadas, basada en el rendimiento y la volatilidad.

    A continuación, se le pedirá que ingrese los símbolos de las acciones y el rango de fechas para el análisis.
    
    Puede consultar tickers en: 
    Yahoo Finance (https://finance.yahoo.com/lookup/) o 
    Nasdaq Symbol Directory (https://www.nasdaq.com/market-activity/stocks/screener)

    """)

    try:
        tickers = input("Ingrese los símbolos (es decír más de uno) de los tickers separados por comas (ejemplo: MSFT, TSLA, NVDA): ").split(",")
        tickers = [ticker.strip().upper() for ticker in tickers]  # Limpiar espacios y convertir a mayúsculas

        date_start = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        date_end = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

        print("\nDescargando datos...")
        try:
            data = downloader.downloader_data(tickers, date_start, date_end)
            data = analyse_data.add_performance(data, tickers)
            
    
                
            if data.empty:
                raise ValueError("No se pudieron descargar datos para los tickers especificados.")
                
        except Exception as e:
            print(f"Error al descargar los datos: {e}")
            return  # Finalizar si la descarga falla

        fin = False
        while not fin:
            print("""\nMenú de opciones:
                  1) Ver estadísticas descriptivas.
                  2) Generar gráficos.
                  3) Calcular peso óptimo.
                  4) Generar informe en documento.
                  5) Salir\n """)
            try:
                opc = int(input("Ingresar opción: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue  # Volver a mostrar el menú si la entrada no es un número

            if opc == 1:
                print("Mostrando análisis descriptivo...")
                try:
                    stats = analyse_data.descriptive(data)
                    # Convertir DataFrame a lista de listas para imprimir con PrettyTable
                    stats.reset_index(inplace=True)
                    stats.columns = ["Ticker"] + stats.columns.tolist()[1:]
                    print_table(stats)
                except Exception as e:
                    print(f"Error al mostrar el análisis descriptivo: {e}")

            elif opc == 2:
                print("""Escoja el tipo de gráfico que desea visualizar:
                      1) Gráfico de series temporales.
                      2) Gráfico de cajas.\n""")
                try:
                    opc = int(input("Elegir opción: "))
                    if opc == 1:
                        analyse_data.show_plot_line_series(data, tickers)
                    elif opc == 2:
                        analyse_data.show_plot_box_plot(data, tickers)
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                except Exception as e:
                    print(f"Error al generar el gráfico: {e}")

            elif opc == 3:
                try:
                    mu, sigma = calculate_weight.calculate_mu_sigma(data, tickers)
                    weights = calculate_weight.calculate_weight(mu, sigma)
                    # Crear DataFrame para mostrar los pesos en tabla
                    weights_df = pd.DataFrame(weights.items(), columns=["Ticker", "Peso Óptimo"])
                    print_table(weights_df)
                except Exception as e:
                    print(f"Error al calcular el peso óptimo: {e}")

            elif opc == 4:

                print("""Opciones:
                      1) Generar informe en un archivo word.
                      2) Generar excel con los datos obtenidos."""
                      )
                opc = int(input("Ingresar opción: "))
                if opc == 1:
                    try:
                        generar_informe(data, tickers, calculate_weight.calculate_weight(mu = calculate_weight.calculate_mu_sigma(data, tickers)[0], sigma=calculate_weight.calculate_mu_sigma(data, tickers)[1]))
                    except Exception as e:
                        print(f"Error al generar el informe: {e}")
                elif opc == 2:
                    try:
                        generar_excel(data)
                    except Exception as e:
                        print(f"Error al generar el excel: {e}")

            elif opc == 5:
                fin = True
                print("Saliendo del programa... ¡Hasta luego!")
            else:
                print("Opción no válida. Intente nuevamente.")

    except Exception as e:
        print(f"Se ha producido un error inesperado: {e}")

if __name__ == "__main__":
    main()
