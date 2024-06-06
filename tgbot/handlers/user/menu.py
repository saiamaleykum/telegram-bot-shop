import asyncpg
import logging
from aiogram import types, Bot
from aiogram.types.input_media_photo import InputMediaPhoto

from keyboards.inline import basic
from db.asyncpg import categories as db_categories
from db.asyncpg.items import get_item, get_items
from db.asyncpg.cart import add_item_to_cart, get_items_from_cart


async def main_menu(
    msg: types.Message, 
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    answer = msg.text
    if answer == "Каталог":
        categories = await db_categories.get_categories(db_pool, db_logger)
        if not categories:
            await msg.answer(text="No categories")
            return
        await msg.answer(
            text="Выберите категорию", 
            reply_markup=basic.categories_paginator("main", 0, categories)
        )
    elif answer == "Корзина":
        items_in_cart = await get_items_from_cart(db_pool, msg.from_user.id, db_logger)
        if not items_in_cart:
            await msg.answer(text="Ваша корзина пуста!")
            return
        m = [
            f"<b>Название:</b> {items_in_cart[0][1]}\n"
            f"<b>Описание:</b> {items_in_cart[0][2]}\n"
            f"<b>Цена:</b> {items_in_cart[0][3]}\n\n"
            f"<b>Кол-во: </b> {items_in_cart[0][0]}"
        ] 
        await msg.answer_photo(
            photo=items_in_cart[0][-1],
            caption="\n".join(m),
            reply_markup=basic.cart_paginator(0, len(items_in_cart), items_in_cart[0][4])
        )
    elif answer == "FAQ":
        await msg.answer("FAQ:", reply_markup=basic.help_keyboard)
    else:
        await msg.answer(text="Я не знаю такое!")


async def categories_handler(
    call: types.CallbackQuery, 
    callback_data: basic.Pagination, 
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    section = str(callback_data.section)
    if section == "main":
        parent_id = 0
        categories = await db_categories.get_categories(db_pool, db_logger)
    elif section == "sub":
        parent_id = callback_data.category_id
        categories = await db_categories.get_subcategories(db_pool, parent_id, db_logger)
    page_num = int(callback_data.page)
    page = page_num - 1 

    if callback_data.action == "next":
        page = page_num + 1 

    await call.message.edit_text(
        text="Выберите категорию",
        reply_markup=basic.categories_paginator(section, page, categories, parent_id)
    )
    await call.answer()


async def to_subcategories(
    call: types.CallbackQuery,
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    parent_id = call.data.split('_')[1]
    subcategories = await db_categories.get_subcategories(db_pool, parent_id, db_logger)
    await call.message.edit_text(
        text="Выберите подкатегорию",
        reply_markup=basic.categories_paginator("sub", 0, subcategories, parent_id)
    )


async def back(
    call: types.CallbackQuery,
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    categories = await db_categories.get_categories(db_pool, db_logger)
    await call.message.delete()
    await call.message.answer(
        text="Выберите категорию",
        reply_markup=basic.categories_paginator("main", 0, categories)
    )


async def to_items(
    call: types.CallbackQuery,
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    subcategory_id = int(call.data.split('_')[1])
    items = await get_items(db_pool, subcategory_id, db_logger)
    m = [
            f"<b>Название:</b> {items[0][0]}\n"
            f"<b>Описание:</b> {items[0][1]}\n"
            f"<b>Цена:</b> {items[0][2]}"
        ] 
    await call.message.answer_photo(
        photo=items[0][-1],
        caption="\n".join(m),
        reply_markup=basic.items_paginator(0, len(items), subcategory_id)
    )


async def item_handler(
    call: types.CallbackQuery, 
    callback_data: basic.Pagination, 
    db_pool: asyncpg.Pool,
    bot: Bot,
    db_logger: logging.Logger
):
    subcategory_id = callback_data.category_id
    items = await get_items(db_pool, subcategory_id, db_logger)
    page_num = int(callback_data.page)
    page = page_num - 1 

    if callback_data.action == "next_item":
        page = page_num + 1 

    m = [
            f"<b>Название:</b> {items[page][1]}\n"
            f"<b>Описание:</b> {items[page][2]}\n"
            f"<b>Цена:</b> {items[page][3]}"
        ] 
    media = InputMediaPhoto(
        media=items[page][-1],
        caption="\n".join(m)
    )
    await bot.edit_message_media(
        media=media,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=basic.items_paginator(page, len(items), subcategory_id, items[page][0])
    )
    await call.answer()


async def to_items(
    call: types.CallbackQuery,
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    subcategory_id = int(call.data.split('_')[1])
    items = await get_items(db_pool, subcategory_id, db_logger)
    await call.message.delete()
    m = [
            f"<b>Название:</b> {items[0][1]}\n"
            f"<b>Описание:</b> {items[0][2]}\n"
            f"<b>Цена:</b> {items[0][3]}"
        ] 
    await call.message.answer_photo(
        photo=items[0][-1],
        caption="\n".join(m),
        reply_markup=basic.items_paginator(0, len(items), subcategory_id, items[0][0])
    )
    await call.answer()


async def input_quantity(
    call: types.CallbackQuery, 
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    item_id = int(call.data.split('_')[2]) 
    item_data = await get_item(db_pool, item_id, db_logger)
    await call.message.delete()
    m = [
            f"<b>Название:</b> {item_data[0]}\n"
            f"<b>Описание:</b> {item_data[1]}\n"
            f"<b>Цена:</b> {item_data[2]}\n\n"
            "Выберите количеcтво"
        ] 
    await call.message.answer_photo(
        photo=item_data[-1],
        caption="\n".join(m),
        reply_markup=basic.quantity_paginator(1, item_id)
    )
    await call.answer()


async def q(call: types.CallbackQuery):
    await call.answer()


async def quantity_handler(
    call: types.CallbackQuery, 
    callback_data: basic.Quantity,
    db_pool: asyncpg.Pool,
    bot: Bot,
    db_logger: logging.Logger
):
    quantity = int(callback_data.quantity)
    item_id = int(callback_data.item_id)
    item_data = await get_item(db_pool, item_id, db_logger)
    quantity_now = quantity - 1 

    if callback_data.action == "quantity_plus":
        quantity_now = quantity + 1 

    m = [
            f"<b>Название:</b> {item_data[0]}\n"
            f"<b>Описание:</b> {item_data[1]}\n"
            f"<b>Цена:</b> {item_data[2]}"
        ] 
    media = InputMediaPhoto(
        media=item_data[-1],
        caption="\n".join(m),
        parse_mode='HTML'
    )
    await bot.edit_message_media(
        media=media,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=basic.quantity_paginator(quantity_now, item_id)
    )
    await call.answer()


async def add_to_cart(
    call: types.CallbackQuery, 
    callback_data: basic.Quantity,
    db_pool: asyncpg.Pool,
    db_logger: logging.Logger
):
    quantity = int(callback_data.quantity)
    item_id = int(callback_data.item_id)
    item_data = await get_item(db_pool, item_id, db_logger)
    user_id = call.from_user.id
    is_exists = await add_item_to_cart(db_pool, user_id, item_id, quantity, db_logger)
    if is_exists:
        m = [
            f"Товар \"{item_data[0]}\" успешно добавлен в вашу корзину!\n\n"
            f"Количество добавленных единиц товара: {quantity}\n\n"
            "Нажмите \"Корзина\" для просмотра"
        ] 
    else:
        m = [
            f"Товар \"{item_data[0]}\" уже был добавлен в вашу корзину!\n\n"
            "Нажмите \"Корзина\" для просмотра"
        ] 
    await call.message.delete()
    await call.message.answer(
        text="\n".join(m)
    )
    await call.answer()


