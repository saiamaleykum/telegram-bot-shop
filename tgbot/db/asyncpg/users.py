import django
import logging
from datetime import datetime
from asgiref.sync import sync_to_async


async def add_user(
    user_model: django.db.models.base.ModelBase,
    user_id: int, 
    username: str, 
    db_logger: logging.Logger
) -> None:
    try:
        await sync_to_async(user_model.objects.get)(user_id=user_id)
    except user_model.DoesNotExist:
        await sync_to_async(user_model.objects.create)(
            user_id=user_id,
            username=username or '',
            time_registration=datetime.now()
        )
    except Exception as e:
        db_logger.error(f"add_user: ({e})")


