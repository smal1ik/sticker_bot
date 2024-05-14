import uuid
import random
from asyncio import sleep
from datetime import timedelta

from aiogram.enums import ChatMemberStatus

from app.database.requests import *

from aiogram import types, F, Router, Bot
import app.utils.keyboards as kb
from aiogram.filters.command import Command

from app.utils import functions
from app.utils.states import Sticker
from aiogram.fsm.context import FSMContext

from arq import ArqRedis
router_main = Router()

@router_main.message(Command("terms"))
async def cmd_start(message: types.Message):
    await message.answer("СОГЛАШЕНИЯ)))")

@router_main.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, arqredis: ArqRedis):
    user = await get_user(message.from_user.id)
    if not user:
        await add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer("Привет! Я пес Коржик из МегаФона. Нажми на “чмок”, чтобы я помог тебе рассказать о чувствах к своей половинке с помощью уникального стикерпака с валентинками.",
                         reply_markup=kb.chpok)
    job = await state.get_data()
    print(job)
    await state.update_data(job="start")
    await state.set_state(Sticker.start)


@router_main.callback_query(Sticker.start, F.data=='chpok')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, arqredis: ArqRedis, bot: Bot):

    job = (await state.get_data())['job']
    await job.abort()

    job = await arqredis.enqueue_job(
        'remind_message', _defer_by=timedelta(minutes=15), chat_id=callback.from_user.id
    )
    await state.update_data(job=job)
    user_channel_status = await bot.get_chat_member(chat_id='@test_smallik1', user_id=callback.from_user.id)
    print(user_channel_status)
    if user_channel_status.status != 'left':
        await callback.message.answer(
            "Это бесплатно, без регистрации и СМС. Ну почти… Нужно только подписаться на канал МегаФона, чтобы стикерпак загрузился со скоростью самого быстрого интернета",
            reply_markup=kb.subscribe)
        await state.set_state(Sticker.name)
        await sleep(1)
        await callback.message.answer(
            "Ну что, начнем магию! Напиши имя или ласковое прозвище, которым ты чаще всего называешь свою «булочку с корицей»!")
    else:
        await callback.message.answer("Кажется ты не подписан",
                             reply_markup=kb.subscribe_with_check)

@router_main.callback_query(F.data=='check_subscribe')
async def check_subscribe(callback: types.CallbackQuery, state: FSMContext, arqredis: ArqRedis, bot: Bot):
    job = (await state.get_data())['job']
    await job.abort()
    job = await arqredis.enqueue_job(
        'remind_message', _defer_by=timedelta(minutes=15), chat_id=callback.from_user.id
    )
    await state.update_data(job=job)

    user_channel_status = await bot.get_chat_member(chat_id='@test_smallik1', user_id=callback.from_user.id)
    if user_channel_status.status != 'left':
        await state.set_state(Sticker.name)
        await callback.message.answer("Ну что, начнем магию! Напиши имя или ласковое прозвище, которым ты чаще всего называешь свою «булочку с корицей»!")
    else:
        await callback.message.answer("Кажется ты не подписан",
                                      reply_markup=kb.subscribe_with_check)


@router_main.message(Sticker.name)
async def answer_message(message: types.Message, state: FSMContext, arqredis: ArqRedis):
    job = (await state.get_data())['job']
    await job.abort()
    job = await arqredis.enqueue_job(
        'remind_message', _defer_by=timedelta(minutes=15), chat_id=message.from_user.id
    )
    await state.update_data(job=job)

    if not message.text:
        await message.answer("Для начала напиши мне прозвище любимки текстом")
    else:
        bad_words = await functions.check_badwords(message.text)
        if bad_words:
            await message.answer("Мат!")
        elif len(message.text) > 15:
            await message.answer("Ого, целая любовная поэма! Столько не смогу забрать, пришли мне прозвище любимки максимум в три слова)")
        else:
            await state.update_data(name=message.text)
            await state.set_state(Sticker.photo)
            await message.answer("Как мило! Хочу скорее увидеть твою половинку! Пришли его / её лучшее фото на свой вкус. Выбирай сердцем! Или нюхом…")

@router_main.callback_query(Sticker.end, F.data=='retry')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, arqredis: ArqRedis):
    job = await arqredis.enqueue_job(
        'remind_message', _defer_by=timedelta(minutes=15), chat_id=callback.from_user.id
    )
    await state.update_data(job=job)
    await state.set_state(Sticker.photo)
    await callback.message.answer("Кидай фото")

@router_main.message(F.photo, Sticker.photo)
async def generate_stickers_set3(message: types.Message, state: FSMContext, bot: Bot, arqredis: ArqRedis):
    job = (await state.get_data())['job']
    await job.abort()

    photo_name = uuid.uuid4().hex
    await message.bot.download(file=message.photo[-1].file_id, destination=f'users_photos/{photo_name}.png')

    n = random.randrange(1, 9999)
    if message.from_user.username == 'None':
        random_name = [random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(5)]
        random_name = "".join(random_name)
        name = f"{random_name}{n}_by_valentinka_megabot"
    else:
        name = f"{message.from_user.username}{n}_by_valentinka_megabot"

    result = await functions.generate_sticker_pack(photo_name)
    if not result:
        await message.answer("Что то пошло не так, попробуй еще раз")
        return

    job = await arqredis.enqueue_job(
        'generate_sticker', _defer_by=timedelta(seconds=2), chat_id=message.from_user.id,
        photo_name=photo_name, name=name
    )
    await message.answer('Создаю для твоей половинки уникальные валентинки! Подожди немного – у меня же лапки…')
    await state.set_state(Sticker.end)
    try:
        await job.result(timeout=90)
    except:
        await message.answer("Попробуй позже, у нас сейчас большая нагрузка", reply_markup=kb.retry)
        await functions.remove_files(photo_name)


@router_main.message(Sticker.photo)
async def generate_stickers_set3(message: types.Message, state: FSMContext, arqredis: ArqRedis):
    job = (await state.get_data())['job']
    await job.abort()
    job = await arqredis.enqueue_job(
        'remind_message', _defer_by=timedelta(minutes=15), chat_id=message.from_user.id
    )
    await state.update_data(job=job)
    await message.answer("На этом этапе нужно прислать мне фотографию. Выбери лучший портрет дорогого тебе человека из фотоплёнки)")

