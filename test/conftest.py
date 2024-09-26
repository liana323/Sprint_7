import pytest
import requests
import random
import string
from helpers import generate_random_string, get_courier_id_service, delete_courier_service # Импорт функции из helpers.py
from locators import COURIER_LOGIN_URL, COURIER_DELETE_URL, COURIER_CREATE_URL
from data import COURIER_DATA

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
    # Оборачиваем вызов функции из helpers.py
    return get_courier_id_service

# Функция для удаления курьера по ID
@pytest.fixture
def delete_courier_by_id():
    # Оборачиваем вызов функции из helpers.py
    return delete_courier_service

# Фикстура для создания данных заказа
@pytest.fixture
def create_order_data():
    def _create_order_data(colors):
        order_data = order_data = COURIER_DATA.copy()
        return order_data
    return _create_order_data