import pytest
import requests

from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from roles.roles import Roles
from models.base_models import TestUser
from models.base_models import TestMovie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST = "92.255.111.76"
PORT = 31200
DATABASE_NAME = "db_movies"
USERNAME = "postgres"
PASSWORD = "AmwFrtnR2"

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope='function')
def test_movie() -> TestMovie:
    random_name = DataGenerator.generate_random_movie_name()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre_id = DataGenerator.generate_genre_id()

    return TestMovie(
        name=random_name,
        imageUrl='https://example.com/image.png',
        price=random_price,
        description=random_description,
        location=random_location,
        published=random_published,
        genreId=random_genre_id,
    )


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        Roles.SUPER_ADMIN.value,
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_dump()
    updated_data.update({
        "verified": True,
        "banned": False,
    })
    updated_user = TestUser(**updated_data)

    return updated_user


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(user_session, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.ADMIN.value),
        new_session
    )

    admin_user.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def id_movie(super_admin, test_movie):
    response = super_admin.api.movie_api.create_movie(test_movie).json()
    id_movie = response['id']
    return id_movie

@pytest.fixture
def http_session():
    session = requests.Session()
    return session

@pytest.fixture
def api_manager(http_session):
    return ApiManager(http_session)

@pytest.fixture(scope="module")
def db_session():
    db_session = SessionLocal()
    yield db_session
    db_session.close()

