from ..config import config

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 49344

WEBHOOK_HOST = 'https://77.82.177.237'
WEBHOOK_PATH = f"/ecoMeet/webhook/{config['bot']['token']}"
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

import pathlib, os

CERT_PATH = os.path.join(pathlib.Path(__file__).resolve().parent, 'certs', 'beautique_cert.pem')
CERT_KEY_PATH = os.path.join(pathlib.Path(__file__).resolve().parent, 'certs', 'beautique_pkey.pem')