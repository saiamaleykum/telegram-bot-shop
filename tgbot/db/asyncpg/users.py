import asyncpg
import logging
from datetime import datetime


async def add_user(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    username: str, 
    db_logger: logging.Logger
) -> None:
    connection = await db_pool.acquire()
    try:
        sql = """
                SELECT user_id 
                FROM users 
                WHERE user_id = $1
                """
        id = await connection.fetchval(sql, user_id)
        if not id:
            sql = """
                INSERT INTO users (user_id, username, time_registration) 
                VALUES ($1, $2, $3)
                """
            await connection.execute(sql, int(user_id), str(username) or '', datetime.now())
    except Exception as e:
        db_logger.error(f"add_user: ({e})")
    finally:
        await db_pool.release(connection)

