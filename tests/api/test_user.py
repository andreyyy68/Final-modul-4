from models.base_models import RegisterUserResponse

import pytest

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        create_user_response = RegisterUserResponse(**response.json())

        assert create_user_response.id != '', "ID должен быть не пустым"
        assert create_user_response.email == creation_user_data.email, "Emil не совпадает"
        assert create_user_response.fullName == creation_user_data.fullName, "Имя не совпадает"
        assert create_user_response.roles == creation_user_data.roles, "Роли не совпадают"
        assert create_user_response.verified is True, 'Верификация не прошла'

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_id = created_user_response['id']

        response_by_id = super_admin.api.user_api.get_user(user_id)
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)

        response = RegisterUserResponse(**response_by_id.json())
        response_email = RegisterUserResponse(**response_by_email.json())

        assert response.email == response_email.email, "Содержание ответов должно быть идентичным"
        assert response.id != '', "ID должен быть не пустым"
        assert response.email == creation_user_data.email, "Email не совпадает"
        assert response.fullName == creation_user_data.fullName, "FullName не совпадает"
        assert response.roles == creation_user_data.roles, "Roles не совпадает"
        assert response.verified is True, 'Верификация не прошла'

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
