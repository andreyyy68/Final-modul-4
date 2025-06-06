import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_str(length):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_movie_name():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    @staticmethod
    def generate_random_image_url():
        return f'"https://example.com/image{random.randint(1, 100)}.png'
    @staticmethod
    def generate_random_price():
        return random.randint(1, 100)
    @staticmethod
    def generate_random_location():
        return random.choice(["SPB", "MSK"])
    @staticmethod
    def generate_random_published():
        return random.choice([True, False])
    @staticmethod
    def generate_genre_id():
        return 1
    @staticmethod
    def generate_description():
        random_description = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return random_description
    @staticmethod
    def generate_random_int():
        random_number = random.randint(1, 100)
        return random_number