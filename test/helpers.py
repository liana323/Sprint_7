# helpers.py
import random
import string
from locators import COURIER_DELETE_URL  # Импортируем COURIER_DELETE_URL

# Функция для генерации случайной строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


import random
import string
import requests
from locators import COURIER_LOGIN_URL


# Функция для генерации случайной строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Метод для получения ID курьера
def get_courier_id_service(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(COURIER_LOGIN_URL, json=payload)

    if response.status_code == 200:
        courier_id = response.json().get('id')
        if courier_id:
            return courier_id
        else:
            raise Exception(f"ID курьера не найдено в ответе: {response.text}")
    else:
        raise Exception(f"Ошибка при логине: {response.status_code}, {response.text}")


# Метод для удаления курьера по ID
def delete_courier_service(courier_id):
    delete_url = f"{COURIER_DELETE_URL}/{courier_id}"
    response = requests.delete(delete_url)

    if response.status_code == 200 and response.json().get("ok"):
        print(f"Курьер с ID {courier_id} был успешно удален.")
    else:
        raise Exception(f"Ошибка при удалении курьера: {response.status_code}, {response.text}")