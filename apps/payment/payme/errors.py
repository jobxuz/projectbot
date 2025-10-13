from enum import Enum

INTERNAL_SERVER_ERROR_MESSAGE = {
    "error": {
        "code": -32400,
        "message":
            {
                "ru": "Internal Server Error",
                "uz": "Internal Server Error",
                "en": "Internal Server Error"
            },
        "data": "Internal Server Error",
    }
}

AUTH_MESSAGE = {
    "error": {
        "code": -32504,
        "message":
            {
                "ru": "Недостаточно привилегий для выполнения метода.",
                "uz": "Usulni bajarish uchun imtiyozlar etarli emas.",
                "en": "You do not have enough privileges to execute the method."
            },
        "data": "You do not have enough privileges to execute the method.",
    }
}

PARSING_JSON_MESSAGE = {
    "error": {
        "code": -32504,
        "message":
            {
                "ru": "Ошибка парсинга JSON.",
                "uz": "JSON parsing error.",
                "en": "JSON parsing error."
            },
        "data": "JSON parsing error.",
    }
}

RPC_METHOD_NOT_FOUND_MESSAGE = {
    "error": {
        "code": -32600,
        "message":
            {
                "ru": "Отсутствуют обязательные поля в RPC-запросе или тип полей не соответствует спецификации.",
                "uz": "JОтсутствуют обязательные поля в RPC-запросе или тип полей не соответствует спецификации.",
                "en": "Отсутствуют обязательные поля в RPC-запросе или тип полей не соответствует спецификации."
            },
        "data": "Отсутствуют обязательные поля в RPC-запросе или тип полей не соответствует спецификации.",
    }
}

RPC_METHOD_NOT_IMPLEMENT_MESSAGE = {
    "error": {
        "code": -32601,
        "message":
            {
                "ru": "Запрашиваемый метод не найден. В RPC-запросе имя запрашиваемого метода содержится в поле data.",
                "uz": "Запрашиваемый метод не найден. В RPC-запросе имя запрашиваемого метода содержится в поле data.",
                "en": "Запрашиваемый метод не найден. В RPC-запросе имя запрашиваемого метода содержится в поле data."
            },
        "data": "Запрашиваемый метод не найден. В RPC-запросе имя запрашиваемого метода содержится в поле data.",
    }
}

TRANSACTION_NOT_FOUND_MESSAGE = {
    "error": {
        "code": -31003,
        "message":
            {
                "ru": "Транзакция не найдена",
                "uz": "Transactsiya topilmadi",
                "en": "transaction not found"
            },
        "data": "transaction not found",
    }
}

INVALID_AMOUNT_MESSAGE = {
    "error": {
        "code": -31001,
        "message":
            {
                "ru": "Неверная сумма",
                "uz": "Miqdori notog'ri",
                "en": "Invalid amount"
            },
        "data": "Invalid amount",
    }
}

ORDER_ALREADY_PAID_MESSAGE = {
    "error": {
        "code": -31051,
        "message":
            {
                "ru": "Заказ уже оплачен",
                "uz": "Buyurtma to‘langan",
                "en": "Order already paid"
            },
        "data": "Order already paid",
    }
}

ORDER_NOT_FOUND_MESSAGE = {
    "error": {
        "code": -31050,
        "message":
            {
                "ru": "Заказ не найден",
                "uz": "Buyurtma topilmadi",
                "en": "Order not found"
            },
        "data": "Order not found",
    }
}
UNABLE_TO_PERFORM_OPERATION_MESSAGE = {
    "error": {
        "code": -31008,
        "message":
            {
                "ru": "Невозможно выполнить данную операцию",
                "uz": "Ushbu amalni bajarib bo'lmaydi",
                "en": "Unable to perform operation"
            },
        "data": "Unable to perform operation",
    }
}


class TransactionStates(int, Enum):
    CREATED = 1
    CLOSED = 2
    CANCELED_CREATED = -1
    CANCELED_CLOSED = -2
