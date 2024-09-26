import requests
import allure
from locators import COURIER_LOGIN_URL
from data import EXPECTED_RESPONSES, ERROR_MESSAGES

@allure.feature('Авторизация курьера')
class TestCourierLogin:
    @allure.title('Успешная авторизация курьера')
    def test_courier_login(self,register_new_courier_and_return_login_password, get_courier_id):
        courier = register_new_courier_and_return_login_password

        with allure.step("Отправляем запрос на авторизацию"):
            response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": courier['password'],
    })
        with allure.step("Проверка"):
            assert response.status_code == EXPECTED_RESPONSES['success_auth'], \
                f"Ожидался код {EXPECTED_RESPONSES['success_auth']}, но получен {response.status_code}"
            assert "id" in response.json(), ERROR_MESSAGES['no_id']

    @allure.title('Авторизация без полей')
    def test_login_without_fields(self):

        response = requests.post(COURIER_LOGIN_URL, data={
        "login": "",
        "password": ""
    })

        with allure.step("Проверка, что система вернула ошибку"):
            assert response.status_code == EXPECTED_RESPONSES['bad_request'], \
                f"Ожидался код {EXPECTED_RESPONSES['bad_request']}, но получен {response.status_code}"
            assert ERROR_MESSAGES['missing_field'] in response.text, ERROR_MESSAGES['missing_field']


    @allure.title('Авторизация без пароля')
    def test_login_without_password(self,register_new_courier_and_return_login_password):
        courier = register_new_courier_and_return_login_password
        response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": ""
    })
        with allure.step("Проверка, что система вернула ошибку"):
            assert response.status_code == EXPECTED_RESPONSES['bad_request'], \
                f"Ожидался код {EXPECTED_RESPONSES['bad_request']}, но получен {response.status_code}"
            assert ERROR_MESSAGES['missing_field'] in response.text, ERROR_MESSAGES['missing_field']


    @allure.title('Авторизация с невалидными данными')
    def test_login_with_invalid_credentials(self,register_new_courier_and_return_login_password):
        courier = register_new_courier_and_return_login_password
        response = requests.post(COURIER_LOGIN_URL, data={
        "login": courier['login'],
        "password": "invalidpass"
    })
        with allure.step("Проверка, что система вернула ошибку"):
            assert response.status_code == EXPECTED_RESPONSES['not_found'], \
                f"Ожидался код {EXPECTED_RESPONSES['not_found']}, но получен {response.status_code}"
            assert ERROR_MESSAGES['account_not_found'] in response.text, ERROR_MESSAGES['account_not_found']
