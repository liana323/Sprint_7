import requests
import allure
from locators import COURIER_LOGIN_URL

@allure.feature('Авторизация')
def test_courier_login(register_new_courier_and_return_login_password, get_courier_id):
    courier = register_new_courier_and_return_login_password

    with allure.step("Отправляем запрос на авторизацию"):
        response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": courier['password'],
    })
    with allure.step("Проверка"):
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert "id" in response.json(), "Ответ не содержит ID курьера"

    courier_id = get_courier_id(courier['login'], courier['password'])
    print(f"ID курьера: {courier_id}")

@allure.feature('Авторизация без полей')
def test_login_without_fields():

    response = requests.post(COURIER_LOGIN_URL, data={
        "login": "",
        "password": ""
    })

    with allure.step("Проверка, что система вернула ошибку"):
       assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"
       assert "Недостаточно данных для входа" in response.text, "Ожидалось сообщение об ошибке"

    print(f"Код ответа: {response.status_code}")


@allure.feature('Авторизицаия без пароля')
def test_login_without_password(register_new_courier_and_return_login_password):
    courier = register_new_courier_and_return_login_password
    response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": ""
    })
    with allure.step("Проверка, что система вернула ошибку"):
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"
        assert "Недостаточно данных для входа" in response.text, "Ожидалось сообщение об ошибке"

    print(f"Код ответа: {response.status_code}")

@allure.feature('Авторизиция с невалидними данными')
def test_login_with_invalid_credentials(register_new_courier_and_return_login_password):
    courier = register_new_courier_and_return_login_password
    response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": "invalidpass"
    })
    with allure.step("Проверка, что система вернула ошибку"):
        assert response.status_code == 404, f"Ожидался код 404, но получен {response.status_code}"
        assert "Учетная запись не найдена" in response.text, "Ожидалось сообщение об ошибке"

    print(f"Код ответа: {response.status_code}")