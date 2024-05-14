from datetime import timedelta

from app.utils import functions
import app.utils.keyboards as kb
from app.utils.config import settings

import os

from arq import Retry

from aiogram import Bot
from aiogram.types.input_sticker import InputSticker
from aiogram.types.input_file import FSInputFile


async def startup(ctx):
    ctx['bot'] = Bot(token=settings.BOT_TOKEN)

async def shutdown(ctx):
    await ctx['bot'].session.close()

async def remind_message(ctx, chat_id):
    remind_msg = """
    На твой телефон пришло новое сообщение. Посмотри, вдруг там что-то важное… Например, создание валентинок для твоей любимки)
    """
    bot: Bot = ctx['bot']
    await bot.send_message(chat_id, remind_msg)

async def generate_sticker(ctx, chat_id, photo_name, name):
    try:
        bot: Bot = ctx['bot']
        url_for_add = f"http://t.me/addstickers/{name}"
        title = "Корги"

        stickers = [
            InputSticker(sticker=FSInputFile(f"C:/Users/motyh/PycharmProjects/sticker_bot/app/generated_stickers/{photo_name}_1.png"), emoji_list=['😀']),
            InputSticker(sticker=FSInputFile(f"C:/Users/motyh/PycharmProjects/sticker_bot/app/generated_stickers/{photo_name}_5.png"), emoji_list=['😀']),]

        # Создание стикер пака
        result = await bot.create_new_sticker_set(
            user_id=chat_id,
            name=name,
            title=title,
            stickers=stickers,
            sticker_format="static")

        await functions.remove_files(photo_name)
        result = await bot.get_sticker_set(name)
        await bot.send_sticker(chat_id, result.stickers[0].file_id)
        await bot.send_message(chat_id, f'Вот твой стикерпак\n{url_for_add}', reply_markup=kb.retry)
    except Exception as e:
        print(e)
        raise Retry(defer=timedelta(seconds=15))

class workersettings:
    max_tries = 3
    redis_settings = settings.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    allow_abort_jobs = True
    functions = [remind_message, generate_sticker, ]