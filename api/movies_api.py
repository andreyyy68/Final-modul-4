from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_ENDPOINT
class MoviesAPI(CustomRequester):
    #Класс для работы с Movie
    def __init__(self, session, base_url, token=None):
        super().__init__(session=session, base_url=base_url, token=token)

    #Проверяем есть ли токен
    def get_auth_token(self):
        if self.token:
            return {'Authorization': f'Bearer {self.token}'}
        return {}

    #Получение списка фильмов
    def getting_movies(self, params, expected_status=200):

        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status,
            params=params or {}
        )

    #Получение фильма по id
    def getting_movie_id(self, movie_id, expected_status=200):

        return self.send_request(
            method="GET",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )
    #Создание нового фильма
    def create_movie(self, test_movie, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=f'{MOVIES_ENDPOINT}',
            data=test_movie,
            expected_status=expected_status,
        )
    #Удаление фильма
    def delete_movie(self, movie_id, expected_status=200):

        headers = self.get_auth_token()

        return self.send_request(
            method="DELETE",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status,
            headers=headers
        )

