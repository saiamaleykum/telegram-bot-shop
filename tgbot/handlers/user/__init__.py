from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command

from states import user
from filters import ChatTypeFilter, TextFilter
from . import start, menu, help, cart, fill_db
from keyboards.inline.basic import Pagination, Quantity, Cart


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter(chat_type="private"))

    user_router.message.register(start.start, CommandStart())
    user_router.message.register(fill_db.fill, Command("fill"))                     # DELETE
    user_router.message.register(menu.main_menu, StateFilter(user.UserMainMenu.menu))
    user_router.callback_query.register(menu.back, F.data == 'back')
    user_router.callback_query.register(
        menu.categories_handler, 
        Pagination.filter(F.action.in_(["prev", "next"]))
    )
    user_router.callback_query.register(menu.to_subcategories, F.data.startswith('main_'))
    user_router.callback_query.register(menu.to_items, F.data.startswith('sub_'))
    user_router.callback_query.register(
        menu.item_handler, 
        Pagination.filter(F.action.in_(["prev_item", "next_item"]))
    )
    user_router.callback_query.register(menu.input_quantity, F.data.startswith('input_quantity_'))
    user_router.callback_query.register(menu.q, F.data == 'q')
    user_router.callback_query.register(
        menu.quantity_handler, 
        Quantity.filter(F.action.in_(["quantity_plus", "quantity_minus"]))
    )
    user_router.callback_query.register(menu.add_to_cart, Quantity.filter(F.action == "add"))

    user_router.callback_query.register(help.help_1, TextFilter('help_1'))
    user_router.callback_query.register(help.help_2, TextFilter('help_2'))
    user_router.callback_query.register(help.help_3, TextFilter('help_3'))
    user_router.callback_query.register(help.help_4, TextFilter('help_4'))
    user_router.callback_query.register(help.help_5, TextFilter('help_5'))
    user_router.callback_query.register(help.help_cancel, TextFilter('cancel'))

    user_router.callback_query.register(
        cart.cart_handler, 
        Cart.filter(F.action.in_(["next_item_in_cart", "prev_item_in_cart"]))
    )
    user_router.callback_query.register(cart.delete_item, F.data.startswith('delete_item_'))
    user_router.callback_query.register(cart.input_address, F.data == "input_address")
    user_router.message.register(cart.making_order, StateFilter(user.UserMainMenu.input_address))

    user_router.callback_query.register(cart.check_handler, F.data.startswith('check_'))

    return user_router
