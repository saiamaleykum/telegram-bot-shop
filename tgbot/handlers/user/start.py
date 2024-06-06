import asyncpg
import logging
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

import states
from keyboards.default.basic import main_keyboard
from db.asyncpg.users import add_user
from data import config


async def check_subscriptions(
    bot: Bot, 
    user_id: int
):
    chat_user_info = await bot.get_chat_member(chat_id=config.CHAT_NAME, user_id=user_id)
    chat_status = chat_user_info.status.value
    channel_user_info = await bot.get_chat_member(chat_id=config.CHANNEL_NAME, user_id=user_id)
    channel_status = channel_user_info.status.value
    if chat_status != 'left' and channel_status != 'left':
        return True
    else: 
        return False


async def start(
    msg: types.Message, 
    state: FSMContext, 
    bot: Bot, 
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    await state.clear()
    if msg.from_user is None:
        return
    m = [
        f"Привет, {msg.from_user.full_name}!\n"
        f"Подпишись на наш чат: {config.CHAT_NAME}\n"
        f"Подпишись на наш канал: {config.CHANNEL_NAME}\n"
    ]
    if await check_subscriptions(bot, msg.from_user.id):
        await add_user(db_pool, msg.from_user.id, msg.from_user.username, db_logger)
        await msg.answer(
            text="Спасибо за подписку!\nВыбери раздел из меню", 
            reply_markup=main_keyboard
        )
        await state.set_state(states.user.UserMainMenu.menu)
    else:
        await msg.answer("\n".join(m))
    
