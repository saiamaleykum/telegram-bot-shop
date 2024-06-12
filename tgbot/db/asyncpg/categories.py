import asyncpg
import logging


async def get_categories(
    db_pool: asyncpg.Pool, 
    db_logger: logging.Logger
) -> list:
    connection = await db_pool.acquire()
    try:
        sql = """
                SELECT category_id, title 
                FROM public.categories
                WHERE parent_id IS NULL
                ORDER BY category_id ASC 
                """
        records = await connection.fetch(sql)
        categories = [[record['category_id'], record['title']] for record in records]
        return categories
    except Exception as e:
        db_logger.error(f"get_categories: ({e})")
    finally:
        await db_pool.release(connection)


async def get_subcategories(
    db_pool: asyncpg.Pool, 
    parent_id: int, 
    db_logger: logging.Logger
) -> list:
    connection = await db_pool.acquire()
    try:
        sql = """
                SELECT category_id, title 
                FROM public.categories
                WHERE parent_id = $1
                """
        records = await connection.fetch(sql, int(parent_id))
        categories = [[record['category_id'], record['title']] for record in records]
        return categories
    except Exception as e:
        db_logger.error(f"get_subcategories: ({e})")
    finally:
        await db_pool.release(connection)