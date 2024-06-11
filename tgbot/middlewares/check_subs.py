from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Update

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


class CheckSubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data.get('bot')
        user_id = data.get('event_chat').id
        result = await check_subscriptions(bot, user_id)

        if result:
            await handler(event, data)
            return     
        else:
            m = [
                f"Подпишись на наш чат: {config.CHAT_NAME}\n"
                f"Подпишись на наш канал: {config.CHANNEL_NAME}\n"
            ]
            await bot.send_message(chat_id=user_id, text="\n".join(m))
            return