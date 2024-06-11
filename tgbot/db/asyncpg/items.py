import asyncpg
import logging


async def get_items(
    db_pool: asyncpg.Pool, 
    category_id: int, 
    db_logger: logging.Logger
) -> list:
    connection = await db_pool.acquire()
    try:
        sql = f"""
                SELECT item_id, title, description, price, photo_id
                FROM items
                WHERE category_id = $1
                ORDER BY category_id ASC 
                """
        records = await connection.fetch(sql, int(category_id))
        categories = [
            [
                record['item_id'], 
                record['title'], 
                record['description'], 
                record['price'],
                record['photo_id']
            ] for record in records
        ]
        return categories
    except Exception as e:
        db_logger.error(f"get_items: ({e})")
    finally:
        await db_pool.release(connection)


async def get_item(
    db_pool: asyncpg.Pool, 
    item_id: int, 
    db_logger: logging.Logger
) -> list:
    connection = await db_pool.acquire()
    try:
        sql = f"""
                SELECT title, description, price, photo_id
                FROM items
                WHERE item_id = $1
                """
        records = await connection.fetch(sql, int(item_id))
        categories = [
            records[0]['title'], 
            records[0]['description'], 
            records[0]['price'],
            records[0]['photo_id']
        ]
        return categories
    except Exception as e:
        db_logger.error(f"get_item: ({e})")
    finally:
        await db_pool.release(connection)