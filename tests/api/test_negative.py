class NegativeMovie:
    def test_create_movie_from_roles(self, common_user, test_movie):
        response = common_user.api.movie_api.create_movie(test_movie)

        assert response.statuse_code == 403, 'Фильм создан с ролью "USER"'
