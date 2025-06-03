from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    MOVIE_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self.session = session
        super().__init__(session, self.MOVIE_BASE_URL)

    def get_movies(self, params=None):
        return self.send_request("GET", "movies", params=params)

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="movies",
            data=data,
            expected_status=expected_status,
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"movies/{movie_id}",
            expected_status=expected_status
        )
