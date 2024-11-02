import anthropic
import requests
from key import API_KEY
import json

client = anthropic.Anthropic(api_key=API_KEY)

url = "https://api.euskadi.eus"
endpoint = "/udalmap/indicators"
params = {
    "summarized": "false",
}

response = requests.get(url + endpoint)

if response.status_code == 200:
    data = response.json()
    indicators = {item["id"]: item["name"] for item in data}
else:
    print("Error obteniendo los indicadores")
    exit()

indicador_que_bucamos = input("Introduce una descrpicion del indicador que buscas: ")

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0,
    system="Eres un experto analista de datos. Responde unicamente con el id.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Aqui tienes los indicadores disponibles en formato `id: nombre`: {indicators}\n Dame el id del indicador cuyo nombre se ajuste mas a la siguiente descripcion: {indicador_que_bucamos}."
                }
            ]
        }
    ]
)

response = message.content
response_content = response[0].text

