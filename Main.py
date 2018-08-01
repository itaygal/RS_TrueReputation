import RunAttacks

if __name__ == '__main__':
    user_movie_ratings = {}
    movie_user_ratings = {}
    movies = set()
    RunAttacks.load(RunAttacks.RATING_PATH, user_movie_ratings, movie_user_ratings, movies)
    movie_release_year = {}
    RunAttacks.load_movie_release_year(movie_release_year)

    RunAttacks.comapre_evaluate_parameter_effectiveness(RunAttacks.ATTACK_RATING_PATH, user_movie_ratings, movie_user_ratings, movies,
                                                        movie_release_year)