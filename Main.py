#=========================================================================================
# Main.py loads rating files, runs attacks on them and compares different reputation algorithms
#=========================================================================================
import RunAttacks

if __name__ == '__main__':
    user_movie_ratings = {}  # dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
    movie_user_ratings = {}  # dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
    movies = set() # set of all movie names
    # load rating .csv file into data structures
    RunAttacks.load(RunAttacks.RATING_PATH, user_movie_ratings, movie_user_ratings, movies)
    # load item information .csv release year into movie release year
    movie_release_year = {}
    RunAttacks.load_movie_release_year(movie_release_year)

    # run all attacks and compare different reputation algorithms
    RunAttacks.run_all_attacks(RunAttacks.ATTACK_RATING_PATH, user_movie_ratings, movie_user_ratings, movies, movie_release_year)

    # compares each different improvements (user age, movie age, const cutoff, percentile cutoff) against attack files
    RunAttacks.comapre_evaluate_parameter_effectiveness(RunAttacks.ATTACK_RATING_PATH, user_movie_ratings, movie_user_ratings, movies,
                                                        movie_release_year)