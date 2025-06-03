import pytest
from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse

def test_register_user(api_manager, creation_user_data):
    response = api_manager.auth_api.register_user(user_data=creation_user_data)
    register_user_response = RegisterUserResponse(**response.json())
    assert register_user_response.email == creation_user_data.email, "Email не совпадает"
