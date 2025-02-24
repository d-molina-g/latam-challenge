from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    with open(file_path, 'r') as archivo:
        lineas = archivo.readlines()
    registros = []
    for entrada in lineas:
        dato = json.loads(entrada)
        dia = datetime.strptime(dato["date"][:10], "%Y-%m-%d").date()
        nombre_usuario = dato["user"]["username"]
        id_tweet = dato["id"]
        registros.append({"date": dia, "user": nombre_usuario, "id": id_tweet})
    df = pd.DataFrame(registros)
    resumen_dias = df.groupby("date").count().sort_values("id", ascending=False).head(10)
    dias_destacados = list(resumen_dias.index)
    df_filtrado = df[df["date"].isin(dias_destacados)]
    df_agrupado = df_filtrado.groupby(["date", "user"]).count().reset_index()
    df_agrupado = df_agrupado.sort_values(["date", "id"], ascending=False)
    df_resultado = df_agrupado.groupby("date").first()
    salida = [(registro.Index, registro.user) for registro in df_resultado[["user"]].itertuples()]
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q1_time(file_path)
    print(resultado)
