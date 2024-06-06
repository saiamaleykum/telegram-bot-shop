import asyncio
import asyncpg
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers, utils
from data import config
from db.asyncpg import create_tables


async def create_db_connections(dp: Dispatcher) -> None:
    logger: logging.Logger = dp["business_logger"]

    logger.debug("Connecting to PostgreSQL")
    try:
        db_pool = await utils.connect_to_services.wait_postgres(
            logger=dp["db_logger"],
            dsn=config.DATABASE_URL
        )
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
    else:
        logger.debug("Succesfully connected to PostgreSQL")
    dp["db_pool"] = db_pool


async def close_db_connections(dp: Dispatcher) -> None:
    if "db_pool" in dp.workflow_data:
        db_pool: asyncpg.Pool = dp["db_pool"]
        await db_pool.close()


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger("aiogram")
    dp["db_logger"] = utils.logging.setup_logger("db")
    dp["business_logger"] = utils.logging.setup_logger("business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await create_db_connections(dp)
    await create_tables(dp['db_pool'] , dp["db_logger"])
    setup_handlers(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await close_db_connections(dispatcher)
    await bot.session.close()
    await dispatcher.storage.close() 
    dispatcher["aiogram_logger"].info("Stopped polling")


def main() -> None:
    bot = Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    if config.USE_WEBHOOK:
        pass
    else:
        dp.startup.register(aiogram_on_startup_polling)
        dp.shutdown.register(aiogram_on_shutdown_polling)
        asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()