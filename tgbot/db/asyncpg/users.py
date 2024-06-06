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
        sql = f"""
                SELECT user_id 
                FROM users 
                WHERE user_id = {user_id}
                """
        id = await connection.fetchval(sql)
        if not id:
            sql = f"""
                INSERT INTO users (user_id, username, time_registration) 
                VALUES ({user_id}, '{username}', '{datetime.now()}')
                """
            await connection.execute(sql)
    except Exception as e:
        db_logger.error(f"add_user: ({e})")
    finally:
        await db_pool.release(connection)

