import requests

from conftest import api_manager_user
from constants import BASE_URL, LOGIN_ENDPOINT
from api.api_manager import ApiManager

class TestNegativeApi:
    def test_negative_auth(self, api_manager_user, test_user):
        data_invalid_password = {
            'email' : test_user['email'],
            'password' : 123
        }

        data_invalid_email ={
            'email' : 'antoshka',
            'password' : test_user['password']
        }
        #Проверка на не валидный пароль
        auth_user = api_manager_user.auth_api.login_user(data_invalid_password, expected_status=500)
        assert auth_user.status_code == 500, 'Авторизация с не валидным паролем'
        print(f'Ошибка: {auth_user.text}')

        #Проверка на не валидный email
        auth_user_invalid_email = api_manager_user.auth_api.login_user(data_invalid_email, expected_status=401)
        assert auth_user_invalid_email.status_code == 401, 'Авторизация с не валидным email'
        print(f'Ошибка: {auth_user_invalid_email.text}')

        #Проверка на авторизацию с пустым телом
        auth_body = api_manager_user.auth_api.login_user({}, expected_status=401)
        assert auth_body.status_code is not 401, 'Авторизация с пустым телом'
