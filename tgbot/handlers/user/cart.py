import asyncpg
import logging
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types.input_media_photo import InputMediaPhoto

import states
from keyboards.inline import basic
from keyboards.default.basic import cancel_keyboard, main_keyboard
from db.asyncpg.cart import delete_all_items_from_cart, delete_item_from_cart, get_items_from_cart
from db.asyncpg.order import create_order
from handlers.user import payment


async def cart_handler(
    call: types.CallbackQuery, 
    callback_data: basic.Cart,
    db_pool: asyncpg.Pool,
    bot: Bot,
    db_logger: logging.Logger
):
    page_num = int(callback_data.page)
    items_in_cart = await get_items_from_cart(db_pool, call.from_user.id, db_logger)
    page = page_num - 1 

    if callback_data.action == "next_item_in_cart":
        page = page_num + 1 

    item_id = int(items_in_cart[page][4])
    m = [
            f"<b>Название:</b> {items_in_cart[page][1]}\n"
            f"<b>Описание:</b> {items_in_cart[page][2]}\n"
            f"<b>Цена:</b> {items_in_cart[page][3]}\n\n"
            f"<b>Кол-во: </b> {items_in_cart[page][0]}"
        ] 
    media = InputMediaPhoto(
        media=items_in_cart[page][-1],
        caption="\n".join(m)
    )
    await bot.edit_message_media(
        media=media,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=basic.cart_paginator(page, len(items_in_cart), item_id)
    )
    await call.answer()


async def delete_item(
    call: types.CallbackQuery, 
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    item_id = int(call.data.split('_')[-1]) 
    await delete_item_from_cart(db_pool, call.from_user.id, item_id, db_logger)
    await call.message.delete()
    await call.message.answer(
        text="Товар успешно удален!"
    )
    await call.answer()


async def input_address(
    call: types.CallbackQuery, 
    state: FSMContext
):
    await call.message.delete()
    await call.message.answer(
        text="Введите адрес для доставки: ",
        reply_markup=cancel_keyboard
    )
    await state.set_state(states.user.UserMainMenu.input_address)
    await call.answer()


async def making_order(
    msg: types.Message, 
    db_pool: asyncpg.Pool, 
    state: FSMContext,
    db_logger: logging.Logger
):
    answer = msg.text
    if answer == "Отменить":
        await msg.answer(
            text="Выберите раздел из меню:", 
            reply_markup=main_keyboard
        )
        await state.set_state(states.user.UserMainMenu.menu)
    else:
        user_id = msg.from_user.id
        items_in_cart = await get_items_from_cart(db_pool, user_id, db_logger)
        payment_sum = 0
        for item in items_in_cart:
            payment_sum += item[0] * item[3]
        await create_order(db_pool, user_id, items_in_cart, answer, db_logger)
        await delete_all_items_from_cart(db_pool, user_id, db_logger)
        payment_url, payment_id = payment.create(payment_sum, msg.chat.id)
        await msg.answer(
            text="Счет для оплаты сформирован", 
            reply_markup=basic.payment_keyboard(payment_url, payment_id)
        )
    

async def check_handler(
    call: types.CallbackQuery,
    state: FSMContext
):
    result = payment.check(call.data.split('_')[-1])
    if result:
        await call.message.answer(
            text="Оплата прошла успешно!", 
            reply_markup=main_keyboard
        )
        await state.set_state(states.user.UserMainMenu.menu)
    else:
        await call.message.answer(
            text="Оплата не прошла или произошла ошибка!"
        )
    await call.answer()