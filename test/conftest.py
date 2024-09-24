import pytest
import requests
import random
import string

from locators import COURIER_LOGIN_URL, COURIER_DELETE_URL, COURIER_CREATE_URL


# Функция для генерации случайной строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Фикстура для создания нового курьера
@pytest.fixture
def register_new_courier_and_return_login_password():
    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на создание курьера с использованием data
    response = requests.post(COURIER_CREATE_URL, data=payload)

    # Если регистрация прошла успешно, добавляем данные в список
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # Логируем ответ для отладки
    print(f"Ответ от API: {response.text}")

    # Передаем данные курьера в тест через yield
    yield {
        "login": login,
        "password": password,
        "firstName": first_name
    }


# Функция для логина курьера и получения его ID
@pytest.fixture
def get_courier_id():
    def _get_courier_id(login, password):
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
    return _get_courier_id

# Функция для удаления курьера по ID
@pytest.fixture
def delete_courier_by_id():
    def _delete_courier_by_id(courier_id):
        delete_url = f"{COURIER_DELETE_URL}/{courier_id}"
        response = requests.delete(delete_url)
        if response.status_code == 200 and response.json().get("ok"):
            print(f"Курьер с ID {courier_id} был успешно удален.")
        else:
            raise Exception(f"Ошибка при удалении курьера: {response.status_code}, {response.text}")
    return _delete_courier_by_id

# Фикстура для создания данных заказа
@pytest.fixture
def create_order_data():
    def _create_order_data(colors):
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": "4",
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": colors  # Цвета
        }
        return order_data
    return _create_order_data