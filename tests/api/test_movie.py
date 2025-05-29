import pytest
import requests

from conftest import api_manager_user, api_manager_admin
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager


class TestMovieAPI:
    def test_get_movie(self, api_manager_user):
        #Получение списка без фильтров
        response = api_manager_user.movies_api.getting_movies(params=None)
        assert response.status_code == 200, 'Список не получен'
        
        #Получение списка с фильтрацией по одному параметру
        response_filter = api_manager_user.movies_api.getting_movies(params={"page" : 1, "pageSize" : 10})
        assert response_filter.status_code == 200, 'Список по фильтрации не получен'
        js_response = response_filter.json()

        #Проверки по фильтрам
        assert "page" in js_response, 'Page нет в ответе'
        assert "pageSize" in js_response, 'pageSize нет в ответе'
        assert js_response["page"] == 1, 'Фильтрация по page некорректна'
        assert js_response["pageSize"] == 10, 'Фильтрация по pageSize некорректна'


    def test_create_movie(self, api_manager_admin, test_movie):
        #Создание фильма
        response = api_manager_admin.movies_api.create_movie(test_movie)
        assert response.status_code == 201, 'Фильм не создан'
        if response.status_code != 201:
            print(response.text)
        response_js = response.json()
        id = response_js["id"]

        response_delete = api_manager_admin.movies_api.delete_movie(id)
        assert response_delete.status_code == 200, 'Ошибка удаления'
        




