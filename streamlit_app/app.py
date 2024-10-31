import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
###########################################################################
from common.downloader import downloader_data
from common.analyse_data import add_performance, descriptive, get_fig_plot_line_series, get_fig_plot_box_plot
from common.calculate_weight import calculate_mu_sigma, calculate_weight
from common.to_generate_word import generar_informe
from common.to_generate_excel import generar_excel
#####################################################################
import streamlit as st
import pandas as pd
import io

st.title("Análisis de Inversión Bursátil")

st.write("""
    Este programa permite realizar un análisis de acciones bursátiles mediante los siguientes conceptos:
    
    1) **Rendimiento Diario**: Cambio porcentual diario en el precio de las acciones.
    2) **Volatilidad**: Mide la variabilidad del precio de las acciones.
    3) **Peso Óptimo**: Distribución óptima de la inversión en las acciones seleccionadas.

    Puede consultar tickers en: [Yahoo Finance](https://finance.yahoo.com/lookup/) o 
    [Nasdaq Symbol Directory](https://www.nasdaq.com/market-activity/stocks/screener)
""")


if "data" not in st.session_state:
    st.session_state["data"] = None
if "tickers_list" not in st.session_state:
    st.session_state["tickers_list"] = None
if "weights" not in st.session_state:
    st.session_state["weights"] = None


tickers = st.text_input("Ingrese los símbolos de los tickers separados por comas (ejemplo: MSFT, TSLA, NVDA)")
date_start = st.date_input("Fecha de inicio")
date_end = st.date_input("Fecha de fin")

tickers_list = [ticker.strip().upper() for ticker in tickers.split(",") if ticker]

if st.button("Analizar"):
    if len(tickers_list) > 0:
        st.write("Descargando datos...")
        try:
            data = downloader_data(tickers_list, date_start, date_end)
            data = add_performance(data, tickers_list)

            if data.empty:
                st.error("No se pudieron descargar datos para los tickers especificados.")
            else:
                st.session_state["data"] = data
                st.session_state["tickers_list"] = tickers_list

                mu, sigma = calculate_mu_sigma(data, tickers_list)
                weights = calculate_weight(mu, sigma)
                st.session_state["weights"] = weights

                st.subheader("Estadísticas Descriptivas")
                stats = descriptive(data)
                st.table(stats)

        except Exception as e:
            st.error(f"Error al descargar o procesar los datos: {e}")
    else:
        st.warning("Por favor, ingrese al menos un símbolo de ticker.")

if "data" in st.session_state and "tickers_list" in st.session_state:
    data = st.session_state["data"]
    tickers_list = st.session_state["tickers_list"]

if st.session_state["data"] is not None and st.session_state["tickers_list"] is not None:
    data = st.session_state["data"]
    tickers_list = st.session_state["tickers_list"]

    st.subheader("Generar Gráficos")
    grafico = st.selectbox("Escoja el tipo de gráfico que desea visualizar", ["Series Temporales", "Box Plot"])

    if grafico == "Series Temporales":
        st.write("Gráfico de Series Temporales")
        fig = get_fig_plot_line_series(data, tickers_list)
        st.pyplot(fig)
    elif grafico == "Box Plot":
        st.write("Gráfico de Box Plot")
        fig = get_fig_plot_box_plot(data, tickers_list)
        st.pyplot(fig)

    if st.session_state["weights"] is not None:
        st.subheader("Peso Óptimo")
        weights_df = pd.DataFrame(st.session_state["weights"].items(), columns=["Ticker", "Peso Óptimo"])
        st.table(weights_df)
    else:
        st.warning("Por favor, realice el análisis primero para calcular los pesos óptimos.")

    st.subheader("Generar y Descargar Informe en Word")
    if st.button("Generar Word"):
        with io.BytesIO() as word_buffer:
            generar_informe(data, tickers_list, st.session_state["weights"], output=word_buffer)
            word_buffer.seek(0)
            st.download_button(
                label="Descargar",
                data=word_buffer,
                file_name="informe_analisis_inversion.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    st.subheader("Generar y Descargar Datos en Excel")
    if st.button("Generar Excel"):
        with io.BytesIO() as excel_buffer:
            generar_excel(data, output=excel_buffer)
            excel_buffer.seek(0)
            st.download_button(
                label="Descargar",
                data=excel_buffer,
                file_name="data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )



# streamlit run streamlit_app/app.py
