import pandas as pd
import os

def generar_excel(data):
    if data.index.dtype == "datetime64[ns, UTC]":
        data.index = data.index.tz_convert(None)  # timezone-unaware

    file_name = "data_download.xlsx"
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="data")
    
        
    file_path = os.path.abspath(file_name)
    print(f"El archivo ha sido guardado como '{file_name}' en '{file_path}'")

