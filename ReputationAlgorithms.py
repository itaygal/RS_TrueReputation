#=========================================================================================
# ReputationAlgorithms.py file holds the implications of different reputation algorithms.
# A reputation algorithm gets all user item ratings and returns a reputation vector (algorithm depended).
# Each reputation vector contains the algorithm reputation for that item.
#
# For example if we had 3 items (movie1, movie2, movie3) a reputation vector of [4, 5, 3] mean that then reputation algorihthm
# have decided that movie1 has a rating of 4, movie2 has a rating of 5 and movie3 has a rating of 3
#
# 3 algorithms are implemented : arithmetic mean, true reputation, true reputation improved
# It test each algorithm implemented in the ReputationAlgorithms.py file (arithmetic mean, true reputation, true reputation improved)
#=========================================================================================

import re
import numpy as np
from numpy import linalg as LA
import sys


""" compute sigmoid function
   Args:
       val: value for sigmoid function
       alpha: alpha set for sigmoid function
       mean: mean for sigmoid function
   Returns:
       sigmoid value
"""
def sigmoid(val, alpha, mean):
    return 1 / (1 + np.exp(-alpha * (val - mean)))


""" computes vector distance (used for change rate)
   Args:
       vec1:  base reputation vector(original ratings)
       vec2:  attacked reputation vector (attacked ratings)
   Returns:
       vector distance
"""
def vector_distance(vec1, vec2):
    return (1 - (np.dot(vec1, vec2) / (
            LA.norm(vec1) * LA.norm(vec2))))

""" original true reputation algorithm originally described in
    "Can You Trust Online Ratings? A Mutual Reinforcement Model for Trustworthy Online Rating Systems"
    
   Args:
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
   Returns:
       true reputation result vector - a vector that contains for each item its new reputations 
"""
def true_reputation(user_movie_ratings, movie_user_ratings, movies):
    # compute user_activity
    user_activity = {}
    # compute user avg rating count
    avg_rating_count = 0.0
    for user_id in user_movie_ratings:
        avg_rating_count += len(user_movie_ratings[user_id])
    avg_rating_count /= len(user_movie_ratings)

    # compute user activity - done only once
    for user_id in user_movie_ratings:
        user_activity[user_id] = sigmoid(len(user_movie_ratings[user_id]), 0.02, avg_rating_count)

    # compute movie stats - for each movie it rating std and mean
    movie_ratings = {}
    movie_stats = {}
    for movie_id in movie_user_ratings:
        movie_ratings[movie_id] = []
        for user_id in movie_user_ratings[movie_id]:
            movie_ratings[movie_id].append(movie_user_ratings[movie_id][user_id][0])
    for movie_id in movie_ratings:
        if len(movie_ratings[movie_id]) > 1:
            movie_stats[movie_id] = [np.mean(movie_ratings[movie_id]), np.std(movie_ratings[movie_id], ddof=1)]
        else:
            movie_stats[movie_id] = [movie_ratings[movie_id][0], movie_ratings[movie_id][0]]

    it_count = 0
    # main loop - run until true reputation is stable
    while True:
        it_count += 1
        # compute user/rating objectivity
        rating_objectivity = {}
        rating_objectivity_list = {}
        user_objectivity = {}
        user_objectivity_normalized = {}
        user_objectivity_mean = 0.0
        for user_id in user_movie_ratings:
            rating_objectivity[user_id] = {}
            rating_objectivity_list[user_id] = []
            user_objectivity[user_id] = 0.0

            for movie_id in user_movie_ratings[user_id]:
                o_r = 0.0
                if movie_stats[movie_id][1] != 0:
                    o_r = abs(
                        (user_movie_ratings[user_id][movie_id][0] - movie_stats[movie_id][0]) / movie_stats[movie_id][
                            1])
                rating_objectivity[user_id][movie_id] = o_r
                rating_objectivity_list[user_id].append(o_r)
                user_objectivity[user_id] += o_r

            user_objectivity[user_id] = user_objectivity[user_id] / len(rating_objectivity[user_id])
            user_objectivity_mean += user_objectivity[user_id]

        user_objectivity_mean /= len(user_objectivity)
        for user_id in user_objectivity:
            user_objectivity_normalized[user_id] = sigmoid(user_objectivity[user_id], -2.5, user_objectivity_mean)

        # Compute user Consistency
        user_consistency = {}
        for user_id in rating_objectivity:
            user_consistency[user_id] = {}
            Q1 = np.percentile(rating_objectivity_list[user_id], 25, interpolation='midpoint')
            Q3 = np.percentile(rating_objectivity_list[user_id], 75, interpolation='midpoint')
            IQR = Q3 - Q1
            for movie_id in rating_objectivity[user_id]:
                o_r = rating_objectivity[user_id][movie_id]
                if (o_r > Q3 + 1.5 * IQR) or (o_r < Q1 - 1.5 * IQR):
                    user_consistency[user_id][movie_id] = 0.0
                elif (o_r <= Q3 + 1.5 * IQR and o_r > Q3 + IQR) or (o_r >= Q1 - 1.5 * IQR and o_r < Q1 - IQR):
                    user_consistency[user_id][movie_id] = 0.5
                elif (o_r <= Q3 + IQR and o_r > Q3 + 0.5 * IQR) or (o_r >= Q1 - IQR and o_r < Q1 - 0.5 * IQR):
                    user_consistency[user_id][movie_id] = 0.7
                elif (o_r <= Q3 + 0.5 * IQR and o_r > Q3) or (o_r >= Q1 - 0.5 * IQR and o_r < Q1):
                    user_consistency[user_id][movie_id] = 0.9
                else:
                    user_consistency[user_id][movie_id] = 1.0

        old_reputation = []
        new_reputation = []
        for movie_id in movies:
            old_reputation.append(movie_stats[movie_id][0])
            movie_stats[movie_id][0] = 0.0
            tr_sum = 0.0
            for user_id in movie_user_ratings[movie_id]:
                tr = user_consistency[user_id][movie_id] * user_activity[user_id] * user_objectivity_normalized[user_id]
                tr_sum += tr
                movie_stats[movie_id][0] += tr * movie_user_ratings[movie_id][user_id][0]
            if tr_sum != 0:
                movie_stats[movie_id][0] /= tr_sum
            new_reputation.append(movie_stats[movie_id][0])

        if vector_distance(new_reputation, old_reputation) < 0.000001: # if stable then return
            return new_reputation


""" improved true reputation algorithm based on algorithm described in
    "Can You Trust Online Ratings? A Mutual Reinforcement Model for Trustworthy Online Rating Systems"
    there 4 improvements: user age, movie age, const cutoff, percentile cutoff 
    By default no improvement will run (the result will be the same as old true reputation)
    see "Improving the True-Reputation Algorithm by Age Parameters" article for more details on each improvement 
    
   Args:
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
       movie_release_year: dic of movie id to movie release year
       APPLAY_USER_SENIORITY: apply user age improvement
       APPLAY_CONST_CUTOFF: apply const cutoff improvement
       APPLAY_PERCENTILE_CUTOFF: apply percentile cutoff improvement
       APPLAY_MOVIE_SENIORITY: apply movie age improvement
       
   Returns:
       improved true reputation result vector - a vector that contains for each item its new reputations 
"""
def true_reputation_improved(user_movie_ratings, movie_user_ratings, movies, movie_release_year, APPLAY_USER_SENIORITY=False,
                             APPLAY_CONST_CUTOFF=False, APPLAY_PERCENTILE_CUTOFF=False, APPLAY_MOVIE_SENIORITY=False):
    if APPLAY_CONST_CUTOFF and APPLAY_PERCENTILE_CUTOFF:  # only one type of cutoff type can be applied
        return
    # compute user_activity
    user_activity = {}
    # compute user avg rating count
    avg_rating_count = 0.0
    for user_id in user_movie_ratings:
        avg_rating_count += len(user_movie_ratings[user_id])
    avg_rating_count /= len(user_movie_ratings)

    # compute user activity
    for user_id in user_movie_ratings:
        user_activity[user_id] = sigmoid(len(user_movie_ratings[user_id]), 0.02, avg_rating_count)

    # compute user seniority
    user_seniority = {}
    if APPLAY_USER_SENIORITY:
        user_seniority_mean = 0.0
        for user_id in user_movie_ratings:
            user_seniority[user_id] = sys.maxsize
            for movie_id in user_movie_ratings[user_id]:
                # divide time stamps by 2592000 (60*60*24*30) to get number of month from 1/1/1970 UTC
                user_seniority[user_id] = min(user_seniority[user_id],
                                              (user_movie_ratings[user_id][movie_id][1] / 2592000))
            user_seniority_mean += user_seniority[user_id]
        user_seniority_mean /= len(user_seniority)
        for user_id in user_seniority:
            user_seniority[user_id] = sigmoid(user_seniority[user_id], -0.2, user_seniority_mean)
    else:
        for user_id in user_movie_ratings:
            user_seniority[user_id] = 1.0

    # compute movie seniority
    movie_seniority = {}
    if APPLAY_MOVIE_SENIORITY:
        movie_release_year_mean = 0.0
        for movie_id in movie_release_year:
            movie_release_year_mean += movie_release_year[movie_id]
        movie_release_year_mean /= len(movie_release_year)
        for movie_id in movies:
            if movie_id not in movie_release_year:
                movie_seniority[movie_id] = sigmoid(movie_release_year_mean, -0.2, movie_release_year_mean)
            else:
                movie_seniority[movie_id] = sigmoid(movie_release_year[movie_id], -0.2, movie_release_year_mean)

    # compute movie stats - for each movie it rating std and mean
    movie_ratings = {}
    movie_stats = {}
    for movie_id in movie_user_ratings:
        movie_ratings[movie_id] = []
        for user_id in movie_user_ratings[movie_id]:
            movie_ratings[movie_id].append(movie_user_ratings[movie_id][user_id][0])
    for movie_id in movie_ratings:
        if len(movie_ratings[movie_id]) > 1:
            movie_stats[movie_id] = [np.mean(movie_ratings[movie_id]), np.std(movie_ratings[movie_id], ddof=1)]
        else:
            movie_stats[movie_id] = [movie_ratings[movie_id][0], movie_ratings[movie_id][0]]

    # main loop
    it_count = 0
    while True:
        it_count += 1
        # compute user/rating objectivity
        rating_objectivity = {}
        rating_objectivity_list = {}
        user_objectivity = {}
        user_objectivity_normalized = {}
        user_objectivity_mean = 0.0
        for user_id in user_movie_ratings:
            rating_objectivity[user_id] = {}
            rating_objectivity_list[user_id] = []
            user_objectivity[user_id] = 0.0

            for movie_id in user_movie_ratings[user_id]:
                o_r = 0.0
                if movie_stats[movie_id][1] != 0:
                    o_r = abs((user_movie_ratings[user_id][movie_id][0] - movie_stats[movie_id][0])
                              / movie_stats[movie_id][1])
                rating_objectivity[user_id][movie_id] = o_r
                rating_objectivity_list[user_id].append(o_r)
                user_objectivity[user_id] += o_r

            user_objectivity[user_id] = user_objectivity[user_id] / len(rating_objectivity[user_id])
            user_objectivity_mean += user_objectivity[user_id]

        user_objectivity_mean /= len(user_objectivity)
        for user_id in user_objectivity:
            user_objectivity_normalized[user_id] = sigmoid(user_objectivity[user_id], -2.5, user_objectivity_mean)

        # User Consistency
        user_consistency = {}
        for user_id in rating_objectivity:
            user_consistency[user_id] = {}
            Q1 = np.percentile(rating_objectivity_list[user_id], 25, interpolation='midpoint')
            Q3 = np.percentile(rating_objectivity_list[user_id], 75, interpolation='midpoint')
            IQR = Q3 - Q1
            for movie_id in rating_objectivity[user_id]:
                o_r = rating_objectivity[user_id][movie_id]
                if (o_r > Q3 + 1.5 * IQR) or (o_r < Q1 - 1.5 * IQR):
                    user_consistency[user_id][movie_id] = 0.0
                elif (o_r <= Q3 + 1.5 * IQR and o_r > Q3 + IQR) or (o_r >= Q1 - 1.5 * IQR and o_r < Q1 - IQR):
                    user_consistency[user_id][movie_id] = 0.5
                elif (o_r <= Q3 + IQR and o_r > Q3 + 0.5 * IQR) or (o_r >= Q1 - IQR and o_r < Q1 - 0.5 * IQR):
                    user_consistency[user_id][movie_id] = 0.7
                elif (o_r <= Q3 + 0.5 * IQR and o_r > Q3) or (o_r >= Q1 - 0.5 * IQR and o_r < Q1):
                    user_consistency[user_id][movie_id] = 0.9
                else:
                    user_consistency[user_id][movie_id] = 1.0
        old_reputation = []
        new_reputation = []
        for movie_id in movies:
            old_reputation.append(movie_stats[movie_id][0])
            movie_stats[movie_id][0] = 0.0
            tr_sum = 0.0
            for user_id in movie_user_ratings[movie_id]:
                tr = user_consistency[user_id][movie_id] * user_objectivity_normalized[user_id] * user_activity[user_id]
                # tr = user_objectivity_normalized[user_id] * user_activity[user_id]
                tr_sum += tr
                movie_stats[movie_id][0] += tr * movie_user_ratings[movie_id][user_id][0]
            if tr_sum != 0:
                movie_stats[movie_id][0] /= tr_sum
            new_reputation.append(movie_stats[movie_id][0])
        # check if stable
        if vector_distance(new_reputation, old_reputation) < 0.000001:
            # apply cutoff optimization
            if APPLAY_CONST_CUTOFF or APPLAY_PERCENTILE_CUTOFF:
                new_reputation.clear()
                # compute final reputation using the cutoff values
                for movie_id in movies:
                    tr_list = []
                    for user_id in movie_user_ratings[movie_id]:
                        tr = user_consistency[user_id][movie_id] * user_objectivity_normalized[user_id] * \
                             user_activity[user_id] * user_seniority[user_id]
                        # tr = user_objectivity_normalized[user_id] * \
                        #      user_activity[user_id] * user_seniority[user_id]
                        tr_list.append([tr, movie_user_ratings[movie_id][user_id][0]])

                    threshold = 0.2 # value for const cutoff improvement
                    if APPLAY_PERCENTILE_CUTOFF:
                        threshold = np.percentile(tr_list, 20, axis=0)[0]  # value for percentile cutoff improvement

                    rating_tr_sum = 0.0
                    tr_sum = 0.0
                    for tr_value, rating in tr_list:
                        if tr_value < threshold:
                            continue
                        tr_sum += tr_value
                        rating_tr_sum += tr_value * rating
                    if tr_sum == 0:
                        new_reputation.append(0)
                    else:
                        new_reputation.append((rating_tr_sum / tr_sum))
            # finally apply movie age improvement
            if APPLAY_MOVIE_SENIORITY:
                for movie_index, movie_id in enumerate(movies, start=0):
                    rating_sum = 0
                    for user_id in movie_user_ratings[movie_id]:
                        rating_sum += movie_user_ratings[movie_id][user_id][0]
                    rating_sum /= len(movie_user_ratings[movie_id])
                    new_reputation[movie_index] = (1 - movie_seniority[movie_id]) * new_reputation[movie_index] + \
                                                  movie_seniority[movie_id] * rating_sum
            return new_reputation

""" arithmetic mean function returns a reputation vector - for each movie the arithmetic mean of its rating is used for its reputation
   Args:
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
   Returns:
       reputation_vector - vector that contains for each movie in "movies" its arithmetic_mean
"""
def arithmetic_mean(movie_user_ratings, movies):
    reputation_vector = []
    for movie_id in movies:
        avg_rating = 0.0
        for user_id in movie_user_ratings[movie_id]:
            avg_rating += movie_user_ratings[movie_id][user_id][0]
        reputation_vector.append(avg_rating / len(movie_user_ratings[movie_id]))
    return reputation_vector

