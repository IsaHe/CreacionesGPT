
import os
import base64
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define el alcance de Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def gmail_authenticate():
    """Autentica y construye el servicio de Gmail usando OAuth 2.0."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'Ocurrió un error al autenticar: {error}')
        return None

def list_messages(service, user_id='me'):
    """Lista los ID de los mensajes en la bandeja de entrada."""
    try:
        results = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'Ocurrió un error al listar mensajes: {error}')
        return []

def get_message(service, user_id, msg_id):
    """Obtiene el contenido de un mensaje específico por ID."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                print(f'Mensaje: {decoded_data}')
    except HttpError as error:
        print(f'Ocurrió un error al obtener el mensaje: {error}')

def monitor_inbox():
    # Autentica y construye el servicio de Gmail
    service = gmail_authenticate()
    if service is None:
        print("No se pudo autenticar.")
        return

    last_seen_id = None

    # Bucle infinito para revisar nuevos correos periódicamente
    while True:
        print("Revisando nuevos mensajes...")
        # Lista los mensajes en la bandeja de entrada
        messages = list_messages(service)
        if not messages:
            print("No se encontraron mensajes.")
        else:
            # Obtiene el ID del mensaje más reciente
            latest_message_id = messages[0]['id']
            print(f"ID del mensaje más reciente: {latest_message_id}")

            # Verifica si hay un mensaje nuevo
            if latest_message_id != last_seen_id:
                print(f"Nuevo mensaje encontrado: ID {latest_message_id}")
                get_message(service, 'me', latest_message_id)
                last_seen_id = latest_message_id  # Actualiza el último ID visto
            else:
                print("No hay mensajes nuevos.")

        # Espera antes de revisar nuevamente (ej. 60 segundos)
        print("Esperando 60 segundos antes de la próxima revisión...")
        time.sleep(60)