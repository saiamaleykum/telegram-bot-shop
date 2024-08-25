# Telegram Bot Shop
## About
**EN**
Telegram Bot Shop with admin panel on Django

**RU**
Магазин в виде телеграм-бота с админ панелью на Django

## Installation
`docker-compose build`

`docker-compose up -d`

## Features 
| Feature | Функция |
| - | - |
| Group/channel subscription check | Проверка подписки на группу/канал |
| Inline menu with pagination | Инлайн меню с пагинацией |
| Payment via YooKassa | Оплата через ЮKassa |
| Uploading orders to excel | Выгрузка заказов в Excel |
| Bulk messaging | Рассылка |
| Logging | Логирование |

| Command | EN | RU |
| - | - | - |
| `/fill` | fill the database with test data | заполнить базу данных тестовыми данными |

[Diagram / Диаграмма](https://ibb.co/jHwyQkw)

[Admin panel / Админ панель](http://localhost:8000/admin/)

## Stack
- Django
- Aiogram
- PostgreSQL (asyncpg)
- Docker
