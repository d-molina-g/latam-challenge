from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q1_memory(file_path: str) -> list:
    particiones = {}
    dir_tmp = "tmp_q1"
    os.makedirs(dir_tmp, exist_ok=True)
    with open(file_path, 'r') as archivo_principal:
        for linea in archivo_principal:
            registro = json.loads(linea)
            fecha = registro.get("date")[:10]
            usuario = registro.get("user").get("username")
            id_tweet = registro.get("id")
            datos = {"usuario": usuario, "id": id_tweet}
            ruta_archivo_temp = os.path.join(dir_tmp, fecha)
            with open(ruta_archivo_temp, "a") as archivo_temp:
                archivo_temp.write(json.dumps(datos) + "\n")
            particiones[fecha] = particiones.get(fecha, 0) + 1
    df_particiones = pd.DataFrame([{"fecha": f, "registros": c} for f, c in particiones.items()])
    df_top10 = df_particiones.sort_values("registros", ascending=False).head(10)
    fechas_top = list(df_top10["fecha"])
    salida = []
    for fecha in fechas_top:
        ruta_temp = os.path.join(dir_tmp, fecha)
        df_temp = pd.read_json(ruta_temp, lines=True)
        df_usuario = df_temp.groupby("usuario").count().sort_values("id", ascending=False)
        usuario_max = df_usuario.index[0]
        salida.append((fecha, usuario_max))
    for nombre_archivo in os.listdir(dir_tmp):
        ruta_temp = os.path.join(dir_tmp, nombre_archivo)
        if os.path.isfile(ruta_temp):
            os.remove(ruta_temp)
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q1_memory(file_path)
    print(resultado)
    
    file_path = sys.argv[1]
    results = q1_memory(file_path)
    for dt, username in results:
        print(f"{dt}: {username}")
