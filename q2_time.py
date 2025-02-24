from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    with open(file_path, 'r') as archivo:
        lineas = archivo.readlines()
    textos = []
    for linea in lineas:
        registro = json.loads(linea)
        textos.append(registro.get("content"))
    todos_emojis = []
    for texto in textos:
        todos_emojis.extend([item.chars for item in emoji.analyze(texto)])
    df_emojis = pd.DataFrame({"emoji": todos_emojis})
    df_emojis["contador"] = 1
    df_top = df_emojis.groupby("emoji").sum().sort_values("contador", ascending=False).head(10)
    df_resultado = df_top.reset_index()
    salida = [(fila["emoji"], fila["contador"]) for _, fila in df_resultado.iterrows()]
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q2_time(file_path)
    print(resultado)