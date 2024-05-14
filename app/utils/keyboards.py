from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

subscribe = InlineKeyboardBuilder()
subscribe.row(
    types.InlineKeyboardButton(
        text="Получить ускорение интернета",
        url="t.me/test_smallik1"),
    width=1
    )
subscribe = subscribe.as_markup()

subscribe_with_check = InlineKeyboardBuilder()
subscribe_with_check.row(
    types.InlineKeyboardButton(
        text="Получить ускорение интернета",
        url="t.me/test_smallik1"),
    types.InlineKeyboardButton(
        text="Я подписался",
        callback_data="check_subscribe"),
    width=1
    )
subscribe_with_check = subscribe_with_check.as_markup()

chpok = InlineKeyboardBuilder()
chpok.row(
    types.InlineKeyboardButton(
        text="чмок",
        callback_data="chpok"),
    width=1
    )
chpok = chpok.as_markup()

retry = InlineKeyboardBuilder()
retry.row(
    types.InlineKeyboardButton(
        text="Попробывать снова",
        callback_data="retry"),
    width=1
    )
retry = retry.as_markup()