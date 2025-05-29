import pytest
import requests

from conftest import registered_user
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager

class TestDeleteAPI:
    def test_delete_user(self, api_manager_admin, registered_user, test_user):
        #Удаляем пользователя по id
        user_id = registered_user["id"]
        response = api_manager_admin.user_api.delete_user(user_id=user_id)
        assert response.status_code == 200, 'Пользователь не удален'
