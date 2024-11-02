from platform import system

import anthropic
import requests
from key import API_KEY
import json
from func import *

client = anthropic.Anthropic(api_key=API_KEY)

url = "https://api.euskadi.eus"
endpoint = "/udalmap/indicators"

response = requests.get(url + endpoint)
if response.status_code == 200:
    data = response.json()
    indicators = {item["id"]: item["name"] for item in data}
else:
    print("Error obteniendo los indicadores")
    exit()

indicador_que_bucamos = input("Introduce una descrpicion del indicador que buscas: ")

response = askCloude(client, "Eres un experto analista de datos. Responde unicamente con el id.", f"Aqui tienes los indicadores disponibles en formato `id: nombre`: {indicators}\n Dame el id del indicador cuyo nombre se ajuste mas a la siguiente descripcion: {indicador_que_bucamos}.")
response_content = response[0].text

response = requests.get(url + endpoint + "/" + response_content)
if response.status_code == 200:
    data = response.json()
else:
    print("Error obteniendo los datos del indicador")
    exit()


nivel_analisis = input("Introduce el nivel de analisis que buscas (entidad, region o municipio): ")
mensaje = "Te voy a dar una serie de entidades junto con su " + data["name"] + " por años en formato: 'nombre': años. Dame un analisis profundo de estos datos.\n"
system = "Eres un experto analista de datos. Responde unicamente con tu analisis profundo de los datos."
match nivel_analisis:
    case "entidad":
        entidades = {item["name"]: item["years"] for item in data["entities"]}
        response = askCloude(client, system, mensaje + f"Entidades: {entidades}")
    case "region":
        regiones = {item["name"]: item["years"] for item in data["regions"]}
        response = askCloude(client, system, mensaje + f"Regiones: {regiones}")
    case "municipio":
        municipios = {item["name"]: item["years"] for item in data["municipalities"]}
        response = askCloude(client, system, mensaje + f"Municipios: {municipios}")

response_content = response[0].text
print(response_content)
