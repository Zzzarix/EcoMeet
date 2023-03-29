from ..config import config

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8443

WEBHOOK_HOST = f'https://188.225.83.42:8443'
WEBHOOK_PATH = f"/ecoMeet/webhook/{config['bot']['token']}"
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

import pathlib, os

CERT_PATH = os.path.join(pathlib.Path(__file__).resolve().parent, 'certs', 'cert.pem')
CERT_KEY_PATH = os.path.join(pathlib.Path(__file__).resolve().parent, 'certs', 'cert.key')
