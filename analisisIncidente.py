from os import write

import requests
import json

url = "https://api.euskadi.eus/traffic"
endpoint = "/v1.0/incidences"

try:
    with open("accidentes.json", "r") as file:
        accidentes = json.load(file)
except FileNotFoundError:
    accidentes = []

def accidente_existe(nuevo_accidente, lista_accidentes):
    for accidente in lista_accidentes:
        if accidente["incidenceId"] == nuevo_accidente["incidenceId"] and accidente["sourceId"] == nuevo_accidente["sourceId"]:
            return True
    return False

for i in range(10):
    response = requests.get(url + endpoint, params={"page": i})
    if response.status_code != 200:
        print("Error obteniendo los datos de las incidencias")
        exit()

    data = response.json()
    for item in data["incidences"]:
        print(item)
        if item["incidenceType"] == "Accidente":
            if accidente_existe(item, accidentes):
                print("El accidente ya existe")
                break

            print("Guardando datos del accidente")
            accidentes.append(item)

with open("accidentes.json", "w") as file:
    file.write(json.dumps(accidentes, indent=4, ensure_ascii=False))
