import threading
from time import sleep

from recibirCorreo import monitor_inbox
import json
from procesarCorreo import getResponse, send_email

def start_monitoring_thread():
    monitoring_thread = threading.Thread(target=monitor_inbox)
    monitoring_thread.daemon = True
    monitoring_thread.start()

if __name__ == '__main__':
    start_monitoring_thread()

    last_message_id = None
    sleep(5)  # Espera 5 segundos para asegurarse de que el hilo de monitoreo haya comenzado
    while True:
        try:
            with open("message.json", "r") as message_file:
                message = json.load(message_file)
        except FileNotFoundError:
            print("Todavía no se ha recibido ningún mensaje")
        except json.JSONDecodeError:
            print("Otro proceso está escribiendo el archivo, intenta de nuevo")

        new_message_id = message["id"]

        if new_message_id != last_message_id:
            print("Nuevo mensaje recibido:")
            print("Asunto:", message["subject"])
            print("Cuerpo:", message["body"])

            print("Procesando respuesta...")
            response = getResponse(message["subject"], message["body"])
            print("Respuesta generada:\n", response)
            send_email(message["from"], "Re: " + message["subject"], response)
            last_message_id = new_message_id