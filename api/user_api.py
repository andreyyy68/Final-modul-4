from custom_requester.custom_requester import CustomRequester
import requests

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session: requests.Session, base_url: str, token=None):
        super().__init__(session=session, base_url=base_url, token=token)

    def get_auth_token(self):
        if self.token:
            return {'Authorization': f'Bearer {self.token}'}
        return {}

    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        headers = self.get_auth_token()

        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
            headers=headers
        )

