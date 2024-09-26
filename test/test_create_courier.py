import requests
import allure
from locators import COURIER_CREATE_URL
from data import EXPECTED_RESPONSES, ERROR_MESSAGES, COURIER_DATA


@allure.feature('Создание курьера')
class TestCourierCreation:

    @allure.title('Создание нового курьера')
    def test_create_courier(self, register_new_courier_and_return_login_password, get_courier_id, delete_courier_by_id):
        # Получаем данные нового курьера из фикстуры
        courier = register_new_courier_and_return_login_password

        with allure.step("Попытка создать курьера"):
            response = requests.post(COURIER_CREATE_URL, data={
                "login": courier['login'],
                "password": courier['password'],
                "firstName": courier['firstName']
            })

            with allure.step("Получаем ID курьера через логин"):
                courier_id = get_courier_id(courier['login'], courier['password'])

            with allure.step("Удаляем курьера по ID"):
                delete_courier_by_id(courier_id)

            with allure.step("Повторяем создание курьера после удаления"):
                response = requests.post(COURIER_CREATE_URL, data={
                    "login": courier['login'],
                    "password": courier['password'],
                    "firstName": courier['firstName']
                })


        with allure.step("Проверка успешного создания курьера"):
            assert response.status_code == EXPECTED_RESPONSES['success'], \
                ERROR_MESSAGES["expected_status_code"].format(expected=EXPECTED_RESPONSES['success'],
                                                              actual=response.status_code)
            assert response.json()["ok"] is True, "Ответ не содержит 'ok': true"
    @allure.title('Создание курьера без обязательного поля')
    def test_create_courier_without_field(self, register_new_courier_and_return_login_password, get_courier_id, delete_courier_by_id):
        # Используем данные нового курьера из фикстуры
        courier = register_new_courier_and_return_login_password

        with allure.step("Попытка создать курьера без обязательного поля"):
            response = requests.post(COURIER_CREATE_URL, data={
                "login": courier['login']
            })


            # Получаем ID курьера через логин и пароль
            courier_id = get_courier_id(courier['login'], courier['password'])

            # Удаляем курьера по ID
            delete_courier_by_id(courier_id)

        with allure.step("Проверка, что статус код 400, так как отсутствует обязательное поле"):
            assert response.status_code == EXPECTED_RESPONSES['bad_request'], \
                ERROR_MESSAGES["expected_status_code"].format(expected=EXPECTED_RESPONSES['bad_request'],
                                                              actual=response.status_code)

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_duplicate_courier(self, register_new_courier_and_return_login_password, get_courier_id, delete_courier_by_id):
        with allure.step("Получаем данные нового курьера с помощью фикстуры"):
            courier = register_new_courier_and_return_login_password

        with allure.step("Попытка создать курьера"):
            response = requests.post(COURIER_CREATE_URL, data={
                "login": courier['login'],
                "password": courier['password'],
                "firstName": courier['firstName']
            })


            with allure.step("Получаем ID курьера через логин"):
                courier_id = get_courier_id(courier['login'], courier['password'])

            with allure.step("Удаляем курьера по ID"):
                delete_courier_by_id(courier_id)

            with allure.step("Повторяем создание курьера после удаления"):
                response = requests.post(COURIER_CREATE_URL, data={
                    "login": courier['login'],
                    "password": courier['password'],
                    "firstName": courier['firstName']
                })

        with allure.step("Проверка успешного создания курьера"):
            assert response.status_code == 201, f"Первый курьер должен быть создан успешно, но получен {response.status_code}"

        with allure.step("Попытка создать курьера с таким же логином"):
            duplicate_response = requests.post(COURIER_CREATE_URL, data={
                "login": courier['login'],
                "password": courier['password'],
                "firstName": courier['firstName']
            })

        with allure.step("Проверка: ожидаем, что вернётся ошибка 409"):
            assert duplicate_response.status_code == EXPECTED_RESPONSES['conflict'], \
                ERROR_MESSAGES["expected_status_code"].format(expected=EXPECTED_RESPONSES['conflict'],
                                                              actual=duplicate_response.status_code)
            assert ERROR_MESSAGES['login_exists'] in duplicate_response.text, "Сообщение об ошибке должно быть в ответе"

