# servicio_simulado.py

import requests
import json
from datetime import datetime

# URL del servidor central
url = 'http://127.0.0.1:5000/logs'
token = 'token1'  # Token para autenticación

def enviar_log(servicio, nivel, mensaje):
    log = {
        'fecha_evento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'servicio': servicio,
        'nivel': nivel,
        'mensaje': mensaje
    }
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(log), headers=headers)
    print(response.json())

# Enviar logs simulados
enviar_log('Servicio1', 'info', 'Este es un mensaje de información.')
enviar_log('Servicio2', 'error', 'Este es un mensaje de error.')
