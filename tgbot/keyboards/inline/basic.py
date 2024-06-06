from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from typing import Literal
from data import messages


NUM_CAT_IN_MSG = 2


class Pagination(CallbackData, prefix="pag"):
    section: str
    action: str
    page: int
    category_id: int


class Quantity(CallbackData, prefix="qua"):
    action: str
    quantity: int
    item_id: int


class Cart(CallbackData, prefix="cart"):
    action: str
    page: int
    item_id: int


def get_num_pages(len: int):
    num = len // NUM_CAT_IN_MSG
    if (len % NUM_CAT_IN_MSG) != 0:
        num += 1
    return num


def categories_paginator(
    section: Literal["main", "sub"], 
    page: int, 
    categories: list, 
    parent_id: int=0
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(NUM_CAT_IN_MSG):
        with suppress(IndexError):
            index = page * NUM_CAT_IN_MSG + i
            builder.row(
                InlineKeyboardButton(
                    text=categories[index][1], 
                    callback_data=f"{section}_{categories[index][0]}"
                )
            )
    if len(categories) > NUM_CAT_IN_MSG:
        if page == 0:
            builder.row(
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Pagination(
                        section=section, 
                        category_id=parent_id, 
                        action="next", 
                        page=page
                    ).pack()
                )
            )
        elif page == get_num_pages(len(categories)) - 1:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Pagination(
                        section=section, 
                        category_id=parent_id, 
                        action="prev", 
                        page=page
                    ).pack()
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Pagination(
                        section=section, 
                        category_id=parent_id, 
                        action="prev", 
                        page=page
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Pagination(
                        section=section, 
                        category_id=parent_id, 
                        action="next", 
                        page=page
                    ).pack()
                ),
                width=2
            )
    if section == "sub":
        builder.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back"
            )
        )
    return builder.as_markup()


def items_paginator(page: int, amount: int, subcategory_id: int, item_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить в корзину",
            callback_data=f"input_quantity_{item_id}"
        )
    )
    if page == 0:
        builder.row(
            InlineKeyboardButton(
                text=">", 
                callback_data=Pagination(
                    section="item", 
                    action="next_item", 
                    page=page, 
                    category_id=subcategory_id
                ).pack()
            )
        )
    elif page == amount - 1:
        builder.row(
            InlineKeyboardButton(
                text="<", 
                callback_data=Pagination(
                    section="item", 
                    action="prev_item", 
                    page=page, 
                    category_id=subcategory_id
                ).pack()
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="<", 
                callback_data=Pagination(
                    section="item", 
                    action="prev_item", 
                    page=page, 
                    category_id=subcategory_id
                ).pack()
            ),
            InlineKeyboardButton(
                text=">", 
                callback_data=Pagination(
                    section="item", 
                    action="next_item", 
                    page=page, 
                    category_id=subcategory_id
                ).pack()
            ),
            width=2
        )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back"
        )
    )
    return builder.as_markup()


def quantity_paginator(quantity: int, item_id: int):
    builder = InlineKeyboardBuilder()
    if quantity > 1:
        builder.row(
            InlineKeyboardButton(
                text="-", 
                callback_data=Quantity(
                    action="quantity_minus",
                    quantity=quantity,
                    item_id=item_id
                ).pack()
            ),
            InlineKeyboardButton(
                text=str(quantity), 
                callback_data="q"
            ),
            InlineKeyboardButton(
                text="+", 
                callback_data=Quantity(
                    action="quantity_plus",
                    quantity=quantity,
                    item_id=item_id
                ).pack()
            ),
            width=3
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text=str(quantity), 
                callback_data="q"
            ),
            InlineKeyboardButton(
                text="+", 
                callback_data=Quantity(
                    action="quantity_plus",
                    quantity=quantity,
                    item_id=item_id
                ).pack()
            ),
            width=2
        )
    builder.row(
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=Quantity(
                action="add",
                quantity=quantity,
                item_id=item_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back"
        )
    )
    return builder.as_markup()


def cart_paginator(page: int, amount: int, item_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оформить заказ",
            callback_data="input_address"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить товар",
            callback_data=f"delete_item_{item_id}"
        )
    )
    if amount > 1:
        if page == 0:
            builder.row(
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Cart(
                        action="next_item_in_cart", 
                        page=page,
                        item_id=item_id
                    ).pack()
                )
            )
        elif page == amount - 1:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Cart(
                        action="prev_item_in_cart", 
                        page=page,
                        item_id=item_id
                    ).pack()
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Cart(
                        action="prev_item_in_cart", 
                        page=page,
                        item_id=item_id
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Cart(
                        action="next_item_in_cart", 
                        page=page,
                        item_id=item_id
                    ).pack()
                ),
                width=2
            )
    return builder.as_markup()


help_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[  
        [InlineKeyboardButton(text=messages.help1_question, callback_data='help_1')],
        [InlineKeyboardButton(text=messages.help2_question, callback_data='help_2')],
        [InlineKeyboardButton(text=messages.help3_question, callback_data='help_3')],
        [InlineKeyboardButton(text=messages.help4_question, callback_data='help_4')],
        [InlineKeyboardButton(text=messages.help5_question, callback_data='help_5')],
    ]
)

help_keyboard_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='◀️ Назад',callback_data='cancel')]
    ]
) 


def payment_keyboard(payment_url, payment_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оплатить 💳",
            url=payment_url
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Проверить оплату ✅",
            callback_data=f"check_{payment_id}"
        )
    )
    return builder.as_markup()