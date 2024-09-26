
# Данные для создания курьера
COURIER_DATA = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": "4",
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
    "color": ["BLACK"]  # Цвета по умолчанию
}

# data.py

# Ожидаемые коды ответов
EXPECTED_RESPONSES = {
    "success": 201,
    "success_auth":200,
    "conflict": 409,
    "bad_request": 400,
    "not_found": 404,
}

# Сообщения об ошибках
ERROR_MESSAGES = {
    "missing_field": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена",
    "login_exists": "Этот логин уже используется",
    "no_track": "Ответ не содержит track",
    "no_id": "Ответ не содержит ID курьера",
    "expected_status_code": "Ожидался код {expected}, но получен {actual}"
}