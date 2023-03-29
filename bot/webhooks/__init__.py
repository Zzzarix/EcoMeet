from aiogram import types, Dispatcher, Bot
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp.web import Application, run_app
import ssl

from .webhook import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, CERT_KEY_PATH, CERT_PATH
# from .payments import _payment_webhook_handler

CERTIFICATE = types.FSInputFile(path=CERT_PATH)

def start_webhook(dp: Dispatcher, bot: Bot) -> None:
    app = Application(middlewares=[], debug=False)
    setup_application(app, dp, bot=bot)

    SimpleRequestHandler(dp, bot, handle_in_background=True).register(app, WEBHOOK_PATH)

    # app.router.add_post('/AAFrDOcFUcCywfKh_wdFv9Q-8HrxGLrz49I', _payment_webhook_handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(CERT_PATH, CERT_KEY_PATH)

    run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)
    run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
