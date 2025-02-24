from datetime import datetime
from typing import List, Tuple
import emoji
import os
import pandas as pd
import json
import sys

def q2_memory(file_path: str) -> list:
    dir_aux = "tmp_q2"
    os.makedirs(dir_aux, exist_ok=True)
    ruta_aux = os.path.join(dir_aux, "emojis.txt")
    with open(file_path, 'r') as arch_in, open(ruta_aux, "a") as arch_out:
        for linea in arch_in:
            dato = json.loads(linea)
            texto = dato.get("content", "")
            lista_emojis = [item["emoji"] for item in emoji.emoji_list(texto)]
            if lista_emojis:
                arch_out.write("\n".join(lista_emojis) + "\n")
    conteo_emojis = {}
    with open(ruta_aux, "r") as aux:
        for linea in aux:
            car = linea.strip()
            if car:
                conteo_emojis[car] = conteo_emojis.get(car, 0) + 1  
    df_emo = pd.DataFrame({"emoji": list(conteo_emojis.keys()), "cuenta": list(conteo_emojis.values())})
    df_top = df_emo.sort_values("cuenta", ascending=False).head(10)
    salida = [tuple(x) for x in df_top.set_index("emoji").itertuples()]
    os.remove(ruta_aux)
    return salida

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python archivo_name.py <ruta_archivo>")
        sys.exit(1)
    file_path = sys.argv[1]
    resultado = q2_memory(file_path)
    print(resultado)