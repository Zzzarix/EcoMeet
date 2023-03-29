from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging as logger

from .config import config
from .db.base import check_db_conn, close_db_conn
from .routes import register_all_routes
from .webhooks import start_webhook, CERTIFICATE, WEBHOOK_URL
from .misc.storage import MongoStorage


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info('Starting bot')

    await check_db_conn()

    await bot.set_my_commands([
        BotCommand(command='/start', description='Начать сначала'),
        BotCommand(command='/mytask', description='Выбранное задание'),
        BotCommand(command='/answer', description='Предоставить результаты выполенения задания'),
        BotCommand(command='/tasks', description='Выбрать задание'),
    ])

    await bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=CERTIFICATE
    )


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logger.info('Shutting down bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.storage.close()
    await bot.session.close()
    close_db_conn()


def main():
    logger.basicConfig(
        level=logger.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    storage = MongoStorage()
    dp = Dispatcher(storage=storage)

    register_all_routes(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(token=config['bot']['token'], parse_mode='HTML')

    start_webhook(dp, bot)


if __name__ == '__main__':
    main()
