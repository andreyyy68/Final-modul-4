from api.movies_api import MoviesAPI
from constants import BASE_URL, MOVIE_URL
from api.auth_api import AuthAPI
from api.user_api import UserAPI

class ApiManager:
    def __init__(self, session, token=None):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session=session, base_url=BASE_URL,token=token)
        self.movies_api = MoviesAPI(session=session, base_url=MOVIE_URL, token=token)

