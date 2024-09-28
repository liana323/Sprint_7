# helpers.py

import random
import string

# Функция для генерации случайной строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
