import asyncpg
import logging
from datetime import datetime


async def create_order(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    dt: datetime, 
    items_in_cart: list, 
    address: str, 
    db_logger: logging.Logger
) -> int:
    connection = await db_pool.acquire()
    try:
        async with connection.transaction():
            sql = f"""
                    INSERT INTO orders (user_id, time_create, status, address) 
                    VALUES ($1, $2, $3, $4)
                    RETURNING order_id
                    """
            order_id = await connection.fetchval(sql, int(user_id), dt, 'paid', str(address))
            for item in items_in_cart:
                sql = f"""
                        INSERT INTO order_items (order_id, item_id, quantity) 
                        VALUES ($1, $2, $3)
                        """
                await connection.execute(sql, int(order_id), int(item[4]), int(item[0]))
            return order_id 
    except Exception as e:
        db_logger.error(f"create_order: ({e})")
    finally:
        await db_pool.release(connection)