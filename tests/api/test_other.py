import pytest
import datetime
import allure

from pytz import timezone
from models.base_models import MovieDBModel, UserDBModel
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from models.base_models import UserCreateResponse, AccountTransactionTemplate


@allure.epic("Тестирование создания и удаления фильма")
@allure.feature("movie_api")
@allure.description("Этот тест проверяет корректное появление и удаление созданного фильма в БД")
def test_create_delete_movie(super_admin, db_session: Session):
    # как бы выглядел SQL запрос
    """SELECT id, "name", price, description, image_url, "location", published, rating, genre_id, created_at
       FROM public.movies
       WHERE name='Test Moviej1h8qss9s5';"""

    movie_name = f"Test Movie{DataGenerator.generate_random_str(10)}"
    movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)

    with allure.step('Проверяем что до начала тестирования фильма с таким названием нет'):
      assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

    movie_data = {
        "name": movie_name,
        "price": 500,
        "description": "Описание тестового фильма",
        "location": "MSK",
        "published": True,
        "genreId": 3
    }
    response = super_admin.api.movie_api.create_movie(
        data=movie_data,
    )
    assert response.status_code == 201, "Фильм должен успешно создаться"
    response = response.json()

    with allure.step('Проверяем, что, после создания, фильм появился в БД'):
       movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
    assert movies_from_db.count() == 1, "В базе уже присутствует фильм с таким названием"

    movie_from_db = movies_from_db.first()
    # можете обратить внимание что в базе данных етсь поле created_at которое мы не здавали явно
    # наш сервис сам его заполнил. проверим что он заполнил его верно с погрешностью в 5 минут
    assert movie_from_db.created_at >= (
                datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(
            minutes=5)), "Сервис выставил время создания с большой погрешностью"

    with allure.step('Удаление фильма из БД'):
       delete_response = super_admin.api.movie_api.delete_movie(movie_id=response["id"])
    assert delete_response.status_code == 200, "Фильм должен успешно удалиться"

    with allure.step('Удаленного фильма нет в БД'):
       movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
    assert movies_from_db.count() == 0, "Фильм небыл удален из базы!"

def test_create_new_user(super_admin, db_session: Session, creation_user_data):
    response = super_admin.api.user_api.create_user(creation_user_data)
    response_js = UserCreateResponse(**response.json())
    user_db = db_session.query(UserDBModel).filter(UserDBModel.id == response_js.id)
    assert response.status_code == 201, "Пользователь не создан"
    assert user_db.count() == 1, "В базе нет такого пользователя"


