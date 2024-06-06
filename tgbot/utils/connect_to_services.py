import asyncpg
import logging


async def wait_postgres(
    logger: logging.Logger,
    dsn: str
) -> asyncpg.Pool:
    db_pool = await asyncpg.create_pool(dsn=dsn)
    logger.debug("Connected to PostgreSQL.")
    return db_pool



