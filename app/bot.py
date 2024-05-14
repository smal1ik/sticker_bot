import asyncio
import logging
import sys

from arq.connections import create_pool, RedisSettings
from aiohttp import web
from utils.config import settings
from aiogram import Bot, Dispatcher, types
from handlers.handlers import router_main
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{settings.URL_WEBHOOK}/webhook")

async def main():

    bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
    await bot.delete_webhook()
    dp = Dispatcher()
    dp.include_router(router_main)
    redis_pool = await create_pool(settings.pool_settings)

    await dp.start_polling(bot, polling_timeout=100, arqredis=redis_pool)


    # dp.startup.register(on_startup)
    # app = web.Application()
    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    # )
    #
    # webhook_requests_handler.register(app, path='/webhook')
    # setup_application(app, dp, bot=bot)
    # web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
        # main()
        print("Bot start")
    except KeyboardInterrupt:
        print('Bot stop')
    except Exception as e:
        print(e)

# if __name__ == "__main__":
#     app.on_startup.append(on_startup)
#
#     web.run_app(app, host='0.0.0.0', port=8000)