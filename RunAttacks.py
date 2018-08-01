import ReputationAlgorithms
import re
import copy
import os

RATING_PATH = "D:\\final project\\u.data"
MOVIE_INFO_PATH = "D:\\final project\\u.item"
ATTACK_RATING_PATH = "D:\\final project\\attacks\\"


def load(dataset_path, user_movie_ratings, movie_user_ratings, movies):
    # user id | item id | rating | timestamp
    rating_match = re.compile("\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)")
    with open(dataset_path, 'r') as dataset_file:
        for rating_line in dataset_file:
            m = rating_match.match(rating_line)
            if m:
                user_id = m.group(1)
                movie_id = m.group(2)
                rating = m.group(3)
                timestamp = m.group(4)
                if user_id not in user_movie_ratings:
                    user_movie_ratings[user_id] = {}
                user_movie_ratings[user_id][movie_id] = (int(rating), int(timestamp))
                if movie_id not in movie_user_ratings:
                    movie_user_ratings[movie_id] = {}
                movies.add(movie_id)
                movie_user_ratings[movie_id][user_id] = (int(rating), int(timestamp))


def load_movie_release_year(movie_release_year):
    rating_match = re.compile("\D*(\d+)\|[^\|]*\|\d+\-\w+\-(\d+)\|")
    with open(MOVIE_INFO_PATH, 'r') as dataset_file:
        for rating_line in dataset_file:
            m = rating_match.match(rating_line)
            if m:
                movie_id = m.group(1)
                year = int(m.group(2))
                movie_release_year[movie_id] = year


def load_attack_file(dataset_path, user_movie_ratings, movie_user_ratings, movies):
    import csv
    from dateutil import parser
    import time
    with open(dataset_path, 'r') as csvFile:
        dataSet = list(csv.reader(csvFile))
        for rating_list in dataSet:
            if rating_list[0] == "":
                break
            user_id = rating_list[0]
            movie_id = rating_list[1]
            rating = rating_list[2]
            dt = parser.parse(rating_list[3])
            timestamp = time.mktime(dt.timetuple())
            if user_id not in user_movie_ratings:
                user_movie_ratings[user_id] = {}
            user_movie_ratings[user_id][movie_id] = (float(rating), int(timestamp))
            if movie_id not in movie_user_ratings:
                movie_user_ratings[movie_id] = {}
            movies.add(movie_id)
            movie_user_ratings[movie_id][user_id] = (float(rating), int(timestamp))

#####################################################
def plot_effectivenes_attack_graph_percentile_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')
    pylab.plot(number_of_ratings,user_movie_age_per_cutoff__change_rates, linewidth=2.5, marker='+', color='black')
    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + " percentile cutoff.png")
    pylab.close()

def plot_effectivenes_attack_graph_no_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()

def plot_effectivenes_attack_graph_const_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')
    pylab.plot(number_of_ratings,user_movie_age_const_cutoff__change_rates , linewidth=2.5, marker='+', color='black')
    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + " const cutoff.png")
    pylab.close()

def load_run_effectivenes_attack_file(attack_file_path, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                      user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    user_movie_ratings_attacked = copy.deepcopy(user_movie_ratings)
    movie_user_ratings_attacked = copy.deepcopy(movie_user_ratings)
    load_attack_file(attack_file_path, user_movie_ratings_attacked, movie_user_ratings_attacked, movies)

    true_reputation_vector_attacked = ReputationAlgorithms.true_reputation(user_movie_ratings_attacked, movie_user_ratings_attacked, movies)
    base_change_rate = ReputationAlgorithms.vector_distance(true_reputation_vector_attacked, true_reputation_vector)


    true_reputation_user_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, False)
    user_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_vector_attacked,true_reputation_user_age_vector )

    true_reputation_movie_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, False, False, False, True)
    movie_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_movie_age_vector_attacked, true_reputation_movie_age_vector)

    true_reputation_user_age_movie_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, True)
    user_age_movie_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_vector_attacked, true_reputation_user_age_movie_age_vector)

    true_reputation_user_age_movie_age_const_cutoff_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, True, False, True)
    user_age_movie_age_const_cutoff_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_const_cutoff_vector_attacked, true_reputation_user_age_movie_age_const_cutoff_vector)
    true_reputation_user_age_movie_age_per_cutoff_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, True, True)
    user_age_movie_age_per_cutoff_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_per_cutoff_vector_attacked, true_reputation_user_age_movie_age_per_cutoff_vector)


    mean_vector_attacked = ReputationAlgorithms.base_reputation(movie_user_ratings_attacked, movies)
    mean_change_rate = ReputationAlgorithms.vector_distance(mean_vector_attacked, base_reputation_vector)

    return [mean_change_rate, base_change_rate, user_age_change_rate, movie_age_change_rate, user_age_movie_age_change_rate, user_age_movie_age_const_cutoff_change_rate, user_age_movie_age_per_cutoff_change_rate]

def load_run_all_effectivenes_attack_files(attack_name, attack_dir_path, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                           user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    number_of_ratings = ["5%", "10%", "15%", "20%", "25%", "30%"]
    base_change_rate = []
    mean_change_rate = []
    user_age_change_rates = []
    movie_age_change_rates = []
    user_movie_age_change_rates = []
    user_movie_age_const_cutoff__change_rates = []
    user_movie_age_per_cutoff__change_rates = []


    for filename in sorted(os.listdir(attack_dir_path+".")):
        if filename.endswith(".csv"):
            change_rates = load_run_effectivenes_attack_file(attack_dir_path+filename, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                      user_movie_ratings, movie_user_ratings, movies, movie_release_year)
            mean_change_rate.append(change_rates[0])
            base_change_rate.append(change_rates[1])
            user_age_change_rates.append(change_rates[2])
            movie_age_change_rates.append(change_rates[3])
            user_movie_age_change_rates.append(change_rates[4])
            user_movie_age_const_cutoff__change_rates.append(change_rates[5])
            user_movie_age_per_cutoff__change_rates.append(change_rates[6])

    plot_effectivenes_attack_graph_no_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)
    plot_effectivenes_attack_graph_const_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)
    plot_effectivenes_attack_graph_percentile_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)

def comapre_evaluate_parameter_effectiveness(attacks_dir_path, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    base_reputation_vector = ReputationAlgorithms.base_reputation(movie_user_ratings, movies)
    true_reputation_vector = ReputationAlgorithms.true_reputation(user_movie_ratings, movie_user_ratings, movies)
    true_reputation_user_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, False)
    true_reputation_movie_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, False, False, False, True)
    true_reputation_user_age_movie_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, True)
    true_reputation_user_age_movie_age_const_cutoff_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, True, False, True)
    true_reputation_user_age_movie_age_per_cutoff_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, True, True)

    for attack_dir in ["TargetOnly Nuke 2", "TargetOnly Push 2"]:
        print(attack_dir)
        load_run_all_effectivenes_attack_files(attack_dir, attacks_dir_path + attack_dir + "\\", base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                           user_movie_ratings, movie_user_ratings, movies, movie_release_year)



#####################################################


def plot_attack_graph(attack_name, number_of_ratings, base_change_rate, improved_change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, label='TRUE-REPUTATION')
    pylab.plot(number_of_ratings, improved_change_rates, linewidth=2.5, marker='^', markersize=12, label='TRUE-REPUTATION++')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()

def plot_attack_graph_with_base(attack_name, number_of_ratings, base_change_rate, improved_change_rates, mean_change_rate):
    import pylab
    pylab.plot(number_of_ratings, mean_change_rate, linewidth=2.5, marker='o', markersize=12, label='ARITHMETIC-MEAN', color='red')
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, label='TRUE-REPUTATION')
    pylab.plot(number_of_ratings, improved_change_rates, linewidth=2.5, marker='^', markersize=12, label='TRUE-REPUTATION++')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()

def load_run_attack_file(attack_file_path, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    user_movie_ratings_attacked = copy.deepcopy(user_movie_ratings)
    movie_user_ratings_attacked = copy.deepcopy(movie_user_ratings)
    load_attack_file(attack_file_path, user_movie_ratings_attacked, movie_user_ratings_attacked, movies)

    true_reputation_vector_attacked = ReputationAlgorithms.true_reputation(user_movie_ratings_attacked, movie_user_ratings_attacked, movies)
    base_change_rate = ReputationAlgorithms.vector_distance(true_reputation_vector_attacked, true_reputation_vector)


    true_reputation_improved_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, True)
    improved_change_rate = ReputationAlgorithms.vector_distance(true_reputation_improved_vector_attacked, true_reputation_improved_vector)

    mean_vector_attacked = ReputationAlgorithms.base_reputation(movie_user_ratings_attacked, movies)
    mean_change_rate = ReputationAlgorithms.vector_distance(mean_vector_attacked, base_reputation_vector)

    return [base_change_rate, improved_change_rate, mean_change_rate]


def load_run_all_attack_files(attack_name, attack_dir_path, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    number_of_ratings = ["5%", "10%", "15%", "20%", "25%", "30%"]
    base_change_rate = []
    improved_change_rates = []
    mean_change_rate = []
    base_change_rate_sum = 0.0
    improved_change_rate_sum = 0.0
    mean_change_rate_sum = 0.0
    for filename in sorted(os.listdir(attack_dir_path+".")):
        if filename.endswith(".csv"):
            change_rates = load_run_attack_file(attack_dir_path+filename, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year)

            base_change_rate.append(change_rates[0])
            improved_change_rates.append(change_rates[1])
            mean_change_rate.append(change_rates[2])

            base_change_rate_sum += change_rates[0]
            improved_change_rate_sum += change_rates[1]
            mean_change_rate_sum += change_rates[2]

    plot_attack_graph(attack_name, number_of_ratings, base_change_rate, improved_change_rates)
    plot_attack_graph_with_base(attack_name + " with ARITHMETIC-MEAN", number_of_ratings, base_change_rate, improved_change_rates, mean_change_rate)
    print("ARITHMETIC-MEAN Change Rate AVG: %.10f" % (mean_change_rate_sum/5))
    print("True Reputation Change Rate AVG: %.10f" % (base_change_rate_sum/5))
    print("True Reputation++ Change Rate AVG: %.10f" % (improved_change_rate_sum/5))
    improvement = ((base_change_rate_sum/5 - improved_change_rate_sum/5) / (improved_change_rate_sum/5)) * 100
    print("True Reputation++/True Reputation improvement : %.3f%%" % improvement)

def run_all_attacks(attacks_dir_path, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    base_reputation_vector = ReputationAlgorithms.base_reputation(movie_user_ratings, movies)
    true_reputation_vector = ReputationAlgorithms.true_reputation(user_movie_ratings, movie_user_ratings, movies)
    true_reputation_improved_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, True)

    for attack_dir in sorted(os.listdir(attacks_dir_path+".")):
        print(attack_dir)
        load_run_all_attack_files(attack_dir, attacks_dir_path + attack_dir + "\\", base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year)

