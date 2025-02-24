from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q3_memory(file_path: str) -> list:
    menciones = []
    with open(file_path, "r") as arch:
        for linea in arch:
            dato = json.loads(linea)
            usuarios_mencionados = dato.get("mentionedUsers")
            if usuarios_mencionados:
                menciones.extend([u["username"] for u in usuarios_mencionados])
    df_menc = pd.DataFrame({"usuario": menciones})
    df_menc["contador"] = 1
    df_agrup = df_menc.groupby("usuario").sum()
    df_top = df_agrup.sort_values("contador", ascending=False).head(10)
    salida = [tuple(x) for x in df_top.itertuples()]
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q3_memory(file_path)
    print(resultado)