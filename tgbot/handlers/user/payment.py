import uuid
from yookassa import Configuration, Payment

from data import config


Configuration.account_id = config.ACCOUNT_ID
Configuration.secret_key = config.SECRET_KEY


def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method_data": {
            'type': 'bank_card'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/gmail77bot"
        },
        "capture": True,
        "metadata": {
            'chat_id': chat_id
        },
        "description": "Заказ №1"
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id

def check(payment_id):
    payment = Payment.find_one(payment_id)
    if payment.status == "succeeded":
        return payment.metadata
    else:
        return False