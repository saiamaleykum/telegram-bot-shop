import asyncpg
import logging
from aiogram import types

    
async def fill(
    msg: types.Message, 
    db_pool: asyncpg.Pool, 
    db_logger: logging.Logger
) -> None:
    connection = await db_pool.acquire()
    try:
        sql = """
                INSERT INTO categories (title, parent_id) VALUES 
                ('Электроника', NULL),
                ('Смартфоны', 1),
                ('Ноутбуки', 1),
                ('Телевизоры', 1),
                ('Аудио и видео', 1),
                ('Одежда', NULL),
                ('Мужская одежда', 6),
                ('Женская одежда', 6),
                ('Детская одежда', 6),
                ('Обувь', 6),
                ('Дом и сад', NULL),
                ('Мебель', 11),
                ('Декор', 11),
                ('Садовые принадлежности', 11),
                ('Освещение', 11),
                ('Красота и здоровье', NULL),
                ('Косметика', 16),
                ('Средства по уходу', 16),
                ('Медицинские товары', 16),
                ('Спортивное питание', 16),
                ('Автотовары', NULL),
                ('Автоаксессуары', 21),
                ('Автозапчасти', 21),
                ('Шины и диски', 21),
                ('Автохимия', 21);
                """
        await connection.execute(sql)
        sql = """
                INSERT INTO items (title, description, price, category_id, photo_id) VALUES 

                ('Смартфон A', 'Современный смартфон с высоким разрешением', 299.99, 2, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Смартфон B', 'Мощный смартфон с большим экраном', 399.99, 2, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Смартфон C', 'Компактный смартфон с хорошей камерой', 199.99, 2, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Смартфон D', 'Смартфон с длительным временем работы', 249.99, 2, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Смартфон E', 'Смартфон с поддержкой 5G', 499.99, 2, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Ноутбуки (category_id = 3)
                ('Ноутбук A', 'Мощный ноутбук для работы и игр', 799.99, 3, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Ноутбук B', 'Компактный ноутбук для учебы', 499.99, 3, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Ноутбук C', 'Ноутбук с большим экраном и хорошей батареей', 699.99, 3, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Ноутбук D', 'Бюджетный ноутбук для повседневных задач', 399.99, 3, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Ноутбук E', 'Ноутбук с отличной производительностью', 999.99, 3, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Телевизоры (category_id = 4)
                ('Телевизор A', 'Телевизор с высоким разрешением и большим экраном', 599.99, 4, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Телевизор B', 'Телевизор с поддержкой 4K и Smart TV', 699.99, 4, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Телевизор C', 'Компактный телевизор для кухни', 299.99, 4, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Телевизор D', 'Телевизор с функцией HDR', 799.99, 4, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Телевизор E', 'Телевизор с интегрированным Wi-Fi', 899.99, 4, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),

                -- Аудио и видео (category_id = 5)
                ('Колонки A', 'Беспроводные колонки с хорошим звуком', 99.99, 5, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Наушники B', 'Наушники с шумоподавлением', 149.99, 5, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Проектор C', 'Компактный проектор для домашнего кинотеатра', 299.99, 5, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Саундбар D', 'Саундбар с мощным басом', 199.99, 5, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('AV-ресивер E', 'AV-ресивер с поддержкой Dolby Atmos', 499.99, 5, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Мужская одежда (category_id = 7)
                ('Футболка A', 'Хлопковая футболка с коротким рукавом', 19.99, 7, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Джинсы B', 'Стильные джинсы из денима', 49.99, 7, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Куртка C', 'Легкая ветровка для весны', 79.99, 7, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Рубашка D', 'Классическая рубашка с длинным рукавом', 39.99, 7, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Шорты E', 'Удобные шорты для спорта', 29.99, 7, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),

                -- Женская одежда (category_id = 8)
                ('Платье A', 'Летнее платье с цветочным принтом', 39.99, 8, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Блузка B', 'Шелковая блузка с кружевом', 49.99, 8, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Юбка C', 'Мини-юбка из денима', 29.99, 8, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Кардиган D', 'Уютный кардиган из кашемира', 59.99, 8, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Топ E', 'Топ с открытыми плечами', 19.99, 8, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Детская одежда (category_id = 9)
                ('Детская футболка A', 'Футболка с мультяшным принтом', 14.99, 9, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Детские джинсы B', 'Джинсы для активных детей', 24.99, 9, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Детская куртка C', 'Теплая куртка для зимы', 49.99, 9, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Детская пижама D', 'Удобная пижама для сна', 19.99, 9, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Детские шорты E', 'Шорты для летних игр', 14.99, 9, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Обувь (category_id = 10)
                ('Кроссовки A', 'Спортивные кроссовки для бега', 69.99, 10, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Ботинки B', 'Кожаные ботинки для зимы', 99.99, 10, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Сандалии C', 'Летние сандалии из кожи', 39.99, 10, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Туфли D', 'Классические туфли для офиса', 59.99, 10, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Балетки E', 'Удобные балетки для прогулок', 29.99, 10, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),

                -- Мебель (category_id = 12)
                ('Диван A', 'Удобный диван для гостиной', 499.99, 12, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Стол B', 'Обеденный стол на 6 человек', 299.99, 12, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Кресло C', 'Мягкое кресло для отдыха', 199.99, 12, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Шкаф D', 'Шкаф-купе для одежды', 399.99, 12, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Тумбочка E', 'Тумбочка с выдвижными ящиками', 99.99, 12, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),

                -- Декор (category_id = 13)
                ('Картина A', 'Картина маслом на холсте', 59.99, 13, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Ваза B', 'Керамическая ваза для цветов', 29.99, 13, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Зеркало C', 'Настенное зеркало в раме', 79.99, 13, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Светильник D', 'Настольный светильник', 39.99, 13, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Коврик E', 'Коврик для прихожей', 49.99, 13, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),

                -- Садовые принадлежности (category_id = 14)
                ('Газонокосилка A', 'Электрическая газонокосилка', 199.99, 14, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Лейка B', 'Лейка для полива растений', 9.99, 14, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Грабли C', 'Грабли для сада', 19.99, 14, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Секатор D', 'Секатор для обрезки веток', 29.99, 14, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Шланг E', 'Садовый шланг 20 м', 49.99, 14, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Освещение (category_id = 15)
                ('Люстра A', 'Красивая люстра для гостиной', 199.99, 15, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Настольная лампа B', 'Лампа для рабочего стола', 29.99, 15, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Торшер C', 'Торшер для чтения', 79.99, 15, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Бра D', 'Настенное бра', 49.99, 15, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Ночник E', 'Детский ночник', 19.99, 15, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Косметика (category_id = 17)
                ('Тушь для ресниц A', 'Водостойкая тушь для ресниц', 19.99, 17, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Помада B', 'Матовая помада', 14.99, 17, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Тональный крем C', 'Тональный крем с увлажнением', 29.99, 17, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Пудра D', 'Компактная пудра', 19.99, 17, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Тени для век E', 'Палетка теней для век', 24.99, 17, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),

                -- Средства по уходу (category_id = 18)
                ('Шампунь A', 'Шампунь для сухих волос', 9.99, 18, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Крем для лица B', 'Увлажняющий крем для лица', 19.99, 18, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Лосьон для тела C', 'Лосьон для тела с витамином E', 14.99, 18, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Маска для волос D', 'Восстанавливающая маска для волос', 24.99, 18, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Гель для душа E', 'Гель для душа с ароматом цитрусов', 7.99, 18, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Медицинские товары (category_id = 19)
                ('Термометр A', 'Цифровой термометр', 14.99, 19, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Тонометр B', 'Автоматический тонометр', 49.99, 19, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Аптечка C', 'Домашняя аптечка', 29.99, 19, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Пульсоксиметр D', 'Пульсоксиметр для измерения кислорода в крови', 19.99, 19, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Массажер E', 'Электрический массажер для спины', 59.99, 19, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Спортивное питание (category_id = 20)
                ('Протеин A', 'Сывороточный протеин', 39.99, 20, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Креатин B', 'Креатин моногидрат', 24.99, 20, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('BCAA C', 'Аминокислоты BCAA', 29.99, 20, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Гейнер D', 'Гейнер для набора массы', 49.99, 20, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('L-карнитин E', 'L-карнитин жидкий', 19.99, 20, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),

                -- Автоаксессуары (category_id = 22)
                ('Автомобильный держатель A', 'Держатель для телефона в машину', 9.99, 22, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),
                ('Автомобильное зарядное устройство B', 'Зарядное устройство для телефона', 14.99, 22, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Автомобильный пылесос C', 'Компактный автомобильный пылесос', 29.99, 22, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Чехлы на сиденья D', 'Комплект чехлов для сидений', 49.99, 22, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Органайзер для багажника E', 'Органайзер для багажника', 24.99, 22, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),

                -- Автозапчасти (category_id = 23)
                ('Фильтр масляный A', 'Масляный фильтр для легковых автомобилей', 9.99, 23, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Фильтр воздушный B', 'Воздушный фильтр для легковых автомобилей', 14.99, 23, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Тормозные колодки C', 'Комплект тормозных колодок', 39.99, 23, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Свечи зажигания D', 'Комплект свечей зажигания', 19.99, 23, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Ремень ГРМ E', 'Ремень газораспределительного механизма', 29.99, 23, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Шины и диски (category_id = 24)
                ('Шины зимние A', 'Зимние шины для легковых автомобилей', 99.99, 24, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Шины летние B', 'Летние шины для легковых автомобилей', 89.99, 24, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Диски алюминиевые C', 'Алюминиевые диски для легковых автомобилей', 199.99, 24, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Диски стальные D', 'Стальные диски для легковых автомобилей', 149.99, 24, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Шины всесезонные E', 'Всесезонные шины для легковых автомобилей', 109.99, 24, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ'),

                -- Автохимия (category_id = 25)
                ('Антифриз A', 'Антифриз для системы охлаждения', 19.99, 25, 'AgACAgIAAxkBAALpQWZc0nXJtwjQLijQyK0EDWgIVqcbAAJ73zEbIPbpSjsiPghUWAJJAQADAgADbQADNQQ'),
                ('Моторное масло B', 'Моторное масло синтетическое', 29.99, 25, 'AgACAgIAAxkBAALpRGZc0pMkhQdd0-LLqlXWbv5gFyvEAAJ83zEbIPbpShUvNlDeozvjAQADAgADbQADNQQ'),
                ('Очиститель стекол C', 'Очиститель стекол для автомобиля', 7.99, 25, 'AgACAgIAAxkBAALpSGZc0quqpV8zlXjbOZvZV2w4dHwfAAJ_3zEbIPbpSlnp1vEQIqvHAQADAgADbQADNQQ'),
                ('Смазка WD-40 D', 'Многоцелевая смазка WD-40', 9.99, 25, 'AgACAgIAAxkBAALpPmZc0jtDTE7DZcYu_XaujcsCRkqKAAJ53zEbIPbpSkbxO0Cz7UYDAQADAgADbQADNQQ'),
                ('Шампунь для машины E', 'Шампунь для ручной мойки', 14.99, 25, 'AgACAgIAAxkBAALpRmZc0qTJtjlDfm49egM3gB9HRI0YAAJ93zEbIPbpSraIdxYXBZkxAQADAgADbQADNQQ');

                """
        await connection.execute(sql)
    except Exception as e:
        db_logger.error(f"add_user: ({e})")
    finally:
        await db_pool.release(connection)
        await msg.answer(
            text="Таблицы Категории и Предметы успешно заполнены!"
        )