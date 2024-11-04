from key import API_KEY
import anthropic

import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from recibirCorreo import gmail_authenticate

def askCloude(client, system, prompt):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content

def getResponse(asunto, mensaje):
    client = anthropic.Client(api_key=API_KEY)
    system = "Eres un profesional corporativo llamado Isaac. Responde unicamente con el cuerpo de tu respuesta."
    respuesta = askCloude(client, system, f"Responde al siguiente correo con un registro acorde al mismo:\nAsunto:{asunto}\nMensaje:{mensaje}")
    return respuesta[0].text

def send_email(to, subject, body):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    service = gmail_authenticate()

    msg = MIMEText(body)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}

    try:
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None