import pytest
import requests
import allure
from urls import ORDER_URL
from data import EXPECTED_RESPONSES, ERROR_MESSAGES


@pytest.mark.parametrize("colors", [
    (["BLACK"]),  # Один цвет
    (["BLACK", "GREY"]),  # Два цвета
    ([])  # Без цвета
])
@allure.feature('Создание курьера')
class TestCreationOrder:
    @allure.title('Создание заказа')
    def test_create_order_with_colors(self,create_order_data, colors):

        with allure.step("Генерация данных заказа"):
            order_data = create_order_data(colors)

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(ORDER_URL, json=order_data)


        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == EXPECTED_RESPONSES['success'], \
                f"Ожидался код {EXPECTED_RESPONSES['success']}, но получен {response.status_code}"
            assert "track" in response.json(), ERROR_MESSAGES['no_track']
