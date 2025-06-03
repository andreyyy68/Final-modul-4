import pytest
from models.base_models import MovieResponse
from models.base_models import CreateMovieResponse
class TestMovie:
    @pytest.mark.slow
    def test_get_movie(self, common_user):
        response = common_user.api.movie_api.get_movies()
        response_js = MovieResponse(**response.json())
        assert response.status_code == 200, 'Список фильмов не найден'
        assert response_js.movies[0].id != '', 'Id не пустой'

    @pytest.mark.slow
    def test_get_movie_filter(self, common_user):
        response = common_user.api.movie_api.get_movies(params = {"page" : 1, "pageSize" : 10})
        js_response = response.json()

        assert response.status_code == 200, 'Список фильмов с фильтрацией не получен'
        assert js_response['page'] == 1, 'Фильтрация по page не совпадает'
        assert js_response['pageSize'] == 10, 'Фильтрация по pageSize не совпадает'

    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movie_api.create_movie(test_movie)
        create_response_js = CreateMovieResponse(**response.json())
        assert response.status_code == 201, 'Фильм не создан'
        assert create_response_js.name == test_movie.name, 'Имя не совпадает'

    @pytest.mark.slow
    def test_delete_movie(self, super_admin, id_movie):
        response = super_admin.api.movie_api.delete_movie(id_movie)

        assert response.status_code == 200, 'Фильм не удалился'

    @pytest.mark.xfail
    @pytest.mark.parametrize('id',[10])
    def test_delete_movie_param(self, super_admin, id):
        response = super_admin.api.movie_api.delete_movie(id)

        assert response.status_code == 200, 'Фильм не удалился'

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "price, locations, genreId",
        [
            ((1, 1000), ["SPB", "MSK"], 3)
        ])
    def test_get_movies_filter(self, common_user, price, locations, genreId):
        minPrice, maxPrice = price
        filters = {
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'locations': locations,
            'genreId': genreId
        }
        response = common_user.api.movie_api.get_movies(filters)

        assert response.status_code == 200, 'Фильм по параметрам не найден'
