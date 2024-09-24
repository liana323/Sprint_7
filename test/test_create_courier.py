import requests
import allure
from locators import COURIER_CREATE_URL


@allure.feature('Создание курьера')
def test_create_courier(register_new_courier_and_return_login_password, get_courier_id, delete_courier_by_id):
    # Получаем данные нового курьера из фикстуры
    courier = register_new_courier_and_return_login_password

    with allure.step("Попытка создать курьера"):
        response = requests.post(COURIER_CREATE_URL, data={
            "login": courier['login'],
            "password": courier['password'],
            "firstName": courier['firstName']
        })

    if response.status_code == 201:
        # Успешное создание курьера
        print(f"Курьер создан: {courier['login']}")
    elif response.status_code == 409:
        # Логин уже используется
        print(f"Логин {courier['login']} уже используется. Попытка удаления курьера.")

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

    # Логирование ответа от API
    print(f"Ответ от API: {response.text}")

    with allure.step("Проверка успешного создания курьера"):
        assert response.status_code == 201, f"Ожидался код 201, но получен {response.status_code}"
        assert response.json()["ok"] is True, "Ответ не содержит 'ok': true"


@allure.feature('Попытка создать курьера без обязательного поля')
def test_create_courier_without_field(register_new_courier_and_return_login_password, get_courier_id,
                                      delete_courier_by_id):
    # Используем данные нового курьера из фикстуры
    courier = register_new_courier_and_return_login_password

    with allure.step("Попытка создать курьера без обязательного поля"):
        response = requests.post(COURIER_CREATE_URL, data={
            "login": courier['login']
        })

    if response.status_code == 409:
        print(f"Логин {courier['login']} уже используется. Попытка удаления курьера.")

        # Получаем ID курьера через логин и пароль
        courier_id = get_courier_id(courier['login'], courier['password'])

        # Удаляем курьера по ID
        delete_courier_by_id(courier_id)

    with allure.step("Проверка, что статус код 400, так как отсутствует обязательное поле"):
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"

    with allure.step("Логирование ответа от API для отладки"):
        print(f"Ответ от API: {response.text}")


@allure.feature('Нельзя создать двух одинаковых курьеров')
def test_create_duplicate_courier(register_new_courier_and_return_login_password, get_courier_id, delete_courier_by_id):
    with allure.step("Получаем данные нового курьера с помощью фикстуры"):
        courier = register_new_courier_and_return_login_password

    with allure.step("Попытка создать курьера"):
        response = requests.post(COURIER_CREATE_URL, data={
            "login": courier['login'],
            "password": courier['password'],
            "firstName": courier['firstName']
        })

    if response.status_code == 409:
        print(f"Логин {courier['login']} уже используется. Попытка удаления курьера.")

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
        assert duplicate_response.status_code == 409, "Ожидался код 409, так как логин уже используется"
        assert "Этот логин уже используется" in duplicate_response.text, "Сообщение об ошибке должно быть в ответе"

    print("Тест завершён успешно. Дубликат не создан.")
