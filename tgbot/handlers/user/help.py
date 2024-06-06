from aiogram import types
from keyboards.inline import basic
from data import messages


async def help_1(call: types.CallbackQuery):
    await call.message.edit_text(
        text=messages.help1_message, 
        reply_markup=basic.help_keyboard_cancel
    )


async def help_2(call: types.CallbackQuery):
    await call.message.edit_text(
        text=messages.help2_message, 
        reply_markup=basic.help_keyboard_cancel
    )


async def help_3(call: types.CallbackQuery):
    await call.message.edit_text(
        text=messages.help3_message, 
        reply_markup=basic.help_keyboard_cancel
    )


async def help_4(call: types.CallbackQuery):
    await call.message.edit_text(
        text=messages.help4_message, 
        reply_markup=basic.help_keyboard_cancel
    )


async def help_5(call: types.CallbackQuery):
    await call.message.edit_text(
        text=messages.help5_message, 
        reply_markup=basic.help_keyboard_cancel
    )
 

async def help_cancel(call: types.CallbackQuery):
    await call.message.edit_text(
        text="FAQ:", 
        reply_markup=basic.help_keyboard
    )
