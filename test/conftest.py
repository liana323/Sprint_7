import pytest
import requests
import allure
from urls import COURIER_LOGIN_URL, COURIER_DELETE_URL, COURIER_CREATE_URL
from data import COURIER_DATA
from helpers import generate_random_string  # Импорт функции из helpers.py
from services import get_courier_id_service, delete_courier_service  # Импорт функций из services.py

# Фикстура для создания нового курьера
@pytest.fixture
def register_new_courier_and_return_login_password():
    # Генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на создание курьера
    response = requests.post(COURIER_CREATE_URL, data=payload)

    # Проверяем, что курьер был успешно создан
    assert response.status_code == 201, f"Ожидался код 201, но получен {response.status_code}"

    # Возвращаем данные курьера через yield для использования в тестах
    yield {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Удаляем курьера после выполнения теста
    courier_id = get_courier_id_service(login, password)
    delete_courier_service(courier_id)

# Фикстура для создания данных заказа
@pytest.fixture
def create_order_data():
    def _create_order_data(colors):
        order_data = COURIER_DATA.copy()
        order_data["color"] = colors  # Обновляем цвет в данных
        return order_data
    return _create_order_data
