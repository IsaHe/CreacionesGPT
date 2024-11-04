from os import write

import requests
import json

url = "https://api.euskadi.eus/traffic"
endpoint_accidentes = "/v1.0/incidences"
endpoint_camaras = "v1.0/cameras/byLocation/"
DISTANCIA_DE_BUSQUEDA_KM = 1

def accidente_existe(nuevo_accidente, lista_accidentes):
    for accidente in lista_accidentes:
        if accidente["incidenceId"] == nuevo_accidente["incidenceId"] and accidente["sourceId"] == nuevo_accidente["sourceId"]:
            return True
    return False

def buscar_camaras_cerca(latitud, longitud, distancia_max_accidente):
    camaras = requests.get(url + endpoint_camaras + f"{latitud}/{longitud}/{distancia_max_accidente}")
    return camaras.json()

#--------------- OBTENER LOS ACCIDENTES ---------------
try:
    with open("accidentes.json", "r") as file:
        accidentes = json.load(file)
except FileNotFoundError:
    accidentes = []

for i in range(1, 11):
    response = requests.get(url + endpoint_accidentes, params={"_page" : i})
    if response.status_code != 200:
        print("Error obteniendo los datos de las incidencias")
        exit()

    data = response.json()
    for item in data["incidences"]:
        if item["incidenceType"] == "Accidente" and not accidente_existe(item, accidentes):
            accidentes.append(item)

print("Guardando...")
with open("accidentes.json", "w") as f:
    f.write(json.dumps(accidentes, indent=4, ensure_ascii=False))

#--------------- OBTENER DATOS AL REDEDOR DEL ACCIDENTE ---------------

for accidente in accidentes:
    datos_camaras_cerca = buscar_camaras_cerca(accidente["latitude"], accidente["longitude"], DISTANCIA_DE_BUSQUEDA_KM)
    print("Camaras cercan del accidente " + accidente["incidenceId"] + ":")
    print(json.dumps(datos_camaras_cerca, indent=4, ensure_ascii=False))