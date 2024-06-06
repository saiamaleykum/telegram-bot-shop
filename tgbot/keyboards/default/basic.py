from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
              [KeyboardButton(text='FAQ')]],
    resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отменить')]],
    resize_keyboard=True
)

