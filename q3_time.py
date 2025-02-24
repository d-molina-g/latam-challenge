from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    with open(file_path, 'r') as f:
        registros = f.readlines()
    lista_menciones = []
    for linea in registros:
        datos = json.loads(linea)
        usuarios = datos.get("mentionedUsers")
        if usuarios:
            for usuario in usuarios:
                lista_menciones.append(usuario["username"])
    df_menciones = pd.DataFrame({"usuario": lista_menciones})
    df_menciones["conteo"] = 1
    resumen = df_menciones.groupby("usuario").sum()
    top_10 = resumen.sort_values("conteo", ascending=False).head(10)
    salida = [(fila.Index, fila.conteo) for fila in top_10.itertuples()]
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q3_time(file_path)
    print(resultado)
