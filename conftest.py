from faker import Faker
import pytest
import requests

from api.auth_api import AuthAPI
from constants import BASE_URL, REGISTER_ENDPOINT, MOVIE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
faker = Faker()

@pytest.fixture(scope='session')
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope='session')
def test_movie():
    random_name = DataGenerator.generate_random_movie_name()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre_id = DataGenerator.generate_genre_id()

    return {
        "name": random_name,
        "imageUrl": 'https://example.com/image.png',
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre_id,
    }

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["email"] = response_data.get("email", test_user["email"])
    registered_user["password"] = test_user["password"]
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def http_session_user():
    """
    Фикстура для создания user HTTP-сессии.
    """
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def http_session_admin():
    """
    Фикстура для создания admin HTTP-сессии.
    """
    session = requests.Session()
    yield session
    session.close()

#Админские креды
@pytest.fixture(scope="session")
def admin_creds():
    return {
        'username' : 'api1@gmail.com',
        'password' : 'asdqwe123Q',
    }

#Получение админского токена
@pytest.fixture(scope="session")
def auth_token(http_session_admin, admin_creds):
    auth_api = AuthAPI(http_session_admin)
    return auth_api.authenticate(admin_creds)

#Передача админской сессии
@pytest.fixture(scope="session")
def api_manager_admin(http_session_admin, auth_token):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(http_session_admin, token=auth_token)

#Передача user сессии
@pytest.fixture(scope="session")
def api_manager_user(http_session_user):
    return ApiManager(http_session_user, token=None)

#Получение id созданного фильма
@pytest.fixture(scope="session")
def create_movie_auth(api_manager_admin, test_movie):
    response = api_manager_admin.movies_api.create_movie(test_movie)
    assert response.status_code == 201, 'Фильм не создался'
    js_response = response.json()
    id_movie = js_response["id"]
    yield id_movie



