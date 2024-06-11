import asyncpg
import logging


async def add_item_to_cart(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    item_id: int, 
    quantity: int, 
    db_logger: logging.Logger
) -> bool:
    connection = await db_pool.acquire()
    try:
        async with connection.transaction():
            sql = f"""
                    SELECT quantity 
                    FROM cart 
                    WHERE user_id = $1 AND item_id = $2
                    """
            result = await connection.fetchval(sql, int(user_id), int(item_id))
            if result:
                return False
            else:
                sql = f"""
                    INSERT INTO cart (user_id, item_id, quantity) 
                    VALUES ($1, $2, $3)
                    """
                await connection.execute(sql, int(user_id), int(item_id), int(quantity))
                return True
    except Exception as e:
        db_logger.error(f"add_item_to_cart: ({e})")
    finally:
        await db_pool.release(connection)


async def get_items_from_cart(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    db_logger: logging.Logger
) -> list:
    connection = await db_pool.acquire()
    try:
        sql = f"""
                SELECT c.quantity, i.title, i.description, i.price, c.item_id, i.photo_id
                FROM cart AS c
                LEFT JOIN items AS i ON c.item_id = i.item_id
                WHERE user_id = $1
                ORDER BY c.item_id ASC
                """
        records = await connection.fetch(sql, int(user_id))
        items = [
            [
                record['quantity'],
                record['title'],
                record['description'],
                record['price'],
                record['item_id'],
                record['photo_id']
            ] for record in records
        ]
        return items
    except Exception as e:
        db_logger.error(f"get_items_from_cart: ({e})")
    finally:
        await db_pool.release(connection)


async def delete_item_from_cart(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    item_id: int, 
    db_logger: logging.Logger
) -> None:
    connection = await db_pool.acquire()
    try:
        sql = f"""
                DELETE FROM cart
                WHERE user_id = $1 AND item_id = $2
                """
        await connection.execute(sql, int(user_id), int(item_id))
    except Exception as e:
        db_logger.error(f"delete_item_from_cart: ({e})")
    finally:
        await db_pool.release(connection)


async def delete_all_items_from_cart(
    db_pool: asyncpg.Pool, 
    user_id: int, 
    db_logger: logging.Logger
) -> None:
    connection = await db_pool.acquire()
    try:
        sql = f"""
                DELETE FROM cart
                WHERE user_id = $1
                """
        await connection.execute(sql, int(user_id))
    except Exception as e:
        db_logger.error(f"delete_all_items_from_cart: ({e})")
    finally:
        await db_pool.release(connection)