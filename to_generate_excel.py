import pandas as pd
import os

def generar_excel(data):
    if data.index.dtype == "datetime64[ns, UTC]":
        data.index = data.index.tz_convert(None)  # Convertir el índice a "timezone-unaware"

    file_name = "data_download.xlsx"
    # Crear un objeto de ExcelWriter
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        # Guardar datos originales
        data.to_excel(writer, sheet_name="data")
    
        
    # Obtener y mostrar la ruta completa del archivo guardado
    file_path = os.path.abspath(file_name)
    print(f"El archivo ha sido guardado como '{file_name}' en '{file_path}'")

