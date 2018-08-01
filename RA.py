import random
import datetime


# =========================================================================================
# Generate Set of Target Movies for Push Attack
# Get:
#   Count - Number of Target Movies
def GenerateSetTargetPush(Count):
    # Initialize global set of target movies
    global TargetSet
    TargetSet = set()

    # List of all movies that are appropriate to be target movies for Push Attack
    AppropriateList = []

    # Min number of ratings per target movie
    # (constant number that defined in the article)
    COUNT_RATINGS_MIN = 90

    # Max number of ratings per target movie
    # (constant number that defined in the article)
    COUNT_RATINGS_MAX = 110

    # Minimum average rating of appropriate target movie for Push Attack
    # (constant number that defined empirically after data analyzing)
    RATING_MIN = 3.46

    # Go through Movies in the Dataset and add to list appropriate target movies
    for Movie in Movies.keys():
        # If number of Movie's ratings is appropriate to be a target movie
        if COUNT_RATINGS_MIN <= Movies[Movie][MOVIE_COUNT_RATINGS] <= COUNT_RATINGS_MAX:
            # If Movie's rating is appropriate for a Push Attack
            if Movies[Movie][MOVIE_AVERAGE_RATING] > RATING_MIN:
                # Add Movie to the list of appropriate target movies for Push Attack
                AppropriateList.append(Movie)

                # Set of random indexes of appropriate movies that will be chosen to be target movies
    IndexSet = set()
    while len(IndexSet) < Count:
        IndexSet.add(random.randint(0, len(AppropriateList) - 1))

    # Add random appropriate movies to the target movies set
    for Index in IndexSet:
        TargetSet.add(AppropriateList[Index])


# =========================================================================================


# =========================================================================================
# Generate Set of Target Movies for Nuke Attack
# Get:
#   Count - Number of Target Movies
def GenerateSetTargetNuke(Count):
    # Initialize global set of target movies
    global TargetSet
    TargetSet = set()

    # List of all movies that are appropriate to be target movies for Nuke Attack
    AppropriateList = []

    # Min number of ratings of target movie
    # (constant number that defined in the article)
    COUNT_RATINGS_MIN = 90

    # Max number of ratings of target movie
    # (constant number that defined in the article)
    COUNT_RATINGS_MAX = 110

    # Maximum average rating of appropriate target movie for Nuke Attack
    # (constant number that defined empirically after data analyzing)
    RATING_MAX = 3.46

    # Go through Movies in the Dataset and add to list appropriate target movies
    for Movie in Movies.keys():
        # If number of Movie's ratings is appropriate to be a target movie
        if COUNT_RATINGS_MIN <= Movies[Movie][MOVIE_COUNT_RATINGS] <= COUNT_RATINGS_MAX:
            # If Movie's rating is appropriate for a Nuke Attack
            if Movies[Movie][MOVIE_AVERAGE_RATING] < RATING_MAX:
                # Add Movie to the list of appropriate target movies for Nuke Attack
                AppropriateList.append(Movie)

                # Set of random indexes of appropriate movies that will be chosen to be target movies
    IndexSet = set()
    while len(IndexSet) < Count:
        IndexSet.add(random.randint(0, len(AppropriateList) - 1))

    # Add random appropriate movies to the target movies set
    for Index in IndexSet:
        TargetSet.add(AppropriateList[Index])


# =========================================================================================


# =========================================================================================
# Generate Set of Selected Movies for Push Attack
# Get:
#   1. Count - Number of Selected Movies
def GenerateSetSelectedPush(Count):
    # Initialize global set of selected movies
    global SelectedSet
    SelectedSet = set()

    # List of all movies that are appropriate to be selected movies
    AppropriateList = []

    # Min number of ratings of selected movie for Push Attack
    # (constant number that defined empirically after data analyzing)
    COUNT_RATINGS_MIN = 300

    # Min average rating of selected movie for Push Attack
    # (constant number that defined empirically after data analyzing)
    RATING_MIN = 4

    # Go through Movies in the Dataset and add to list appropriate selected movies
    for Movie in Movies.keys():
        # If number of Movie's ratings is appropriate to be a selected movie
        if Movies[Movie][MOVIE_COUNT_RATINGS] >= COUNT_RATINGS_MIN:
            # If Movie's average rating is appropriate to be a selected movie
            if Movies[Movie][MOVIE_AVERAGE_RATING] >= RATING_MIN:
                # Add Movie to the list of appropriate selected movies for Push Attack
                AppropriateList.append(Movie)

    # Set of random indexes of appropriate movies that will be chosen to be selected movies
    IndexSet = set()
    while len(IndexSet) < Count:
        IndexSet.add(random.randint(0, len(AppropriateList) - 1))

    # Add random appropriate movies to the selected movies set
    for Index in IndexSet:
        SelectedSet.add(AppropriateList[Index])


# =========================================================================================


# =========================================================================================
# Generate Set of Selected Movies for Nuke Attack
# Get:
#   1. Count - Number of Selected Movies
def GenerateSetSelectedNuke(Count):
    # Initialize global set of selected movies
    global SelectedSet
    SelectedSet = set()

    # List of all movies that are appropriate to be selected movies
    AppropriateList = []

    # Min number of ratings of selected movie for Nuke Attack
    # (constant number that defined empirically after data analyzing)
    COUNT_RATINGS_MIN = 130

    # Max average rating of selected movie for Nuke Attack
    # (constant number that defined empirically after data analyzing)
    RATING_MAX = 3

    # Go through Movies in the Dataset and add to list appropriate selected movies
    for Movie in Movies.keys():
        # If number of Movie's ratings is appropriate to be a selected movie
        if Movies[Movie][MOVIE_COUNT_RATINGS] >= COUNT_RATINGS_MIN:
            # If Movie's average rating is appropriate to be a selected movie
            if Movies[Movie][MOVIE_AVERAGE_RATING] <= RATING_MAX:
                # Add Movie to the list of appropriate selected movies for Nuke Attack
                AppropriateList.append(Movie)

    # Set of random indexes of appropriate movies that will be chosen to be selected movies
    IndexSet = set()
    while len(IndexSet) < Count:
        IndexSet.add(random.randint(0, len(AppropriateList) - 1))

    # Add random appropriate movies to the selected movies set
    for Index in IndexSet:
        SelectedSet.add(AppropriateList[Index])


# =========================================================================================


# =========================================================================================
# Generate Set of Filler Movies
# Get:
#   1. Count - Number of Filler Movies
def GenerateSetFiller(Count):
    # Initialize global set of filler movies
    global FillerSet
    FillerSet = set()

    # List of all movies that are appropriate to be filler movies
    AppropriateList = []

    # Go through Movies in the Dataset and add to list appropriate filler movies
    for Movie in Movies.keys():
        if (Movie not in TargetSet) and (Movie not in SelectedSet):
            AppropriateList.append(Movie)

    # Set of random indexes of appropriate movies that will be chosen to be filler movies
    IndexSet = set()
    while len(IndexSet) < Count:
        IndexSet.add(random.randint(0, len(AppropriateList) - 1))

    # Add random appropriate movies to the filler movies set
    for Index in IndexSet:
        FillerSet.add(AppropriateList[Index])


# =========================================================================================


# =========================================================================================
# Generate Date of Rating Attack
# The assumption is that attack was in the last month
# Returns random date in the last 30 days before the last rating in the dataset
def GenerateDate():
    # List of approriate dates
    Dates = []

    # Last rating in the dataset
    Dt = datetime.datetime(1998, 4, 22)

    # Fill list of appropriate dates
    for n in range(1, 30):
        Dt += datetime.timedelta(days=-1)
        Dates.append(Dt)

    # Set random index in the range of Dates length
    Index = random.randint(0, len(Dates) - 1)

    return Dates[Index]


# =========================================================================================


# =========================================================================================
# Generate Target Only Attack Model
# Get:
#   1. Percent - Percentage of attack ratings from overall ratings of the Movie
#   2. Frequency - Amount of ratings per Attack User
#   3. Rating - Rating that will given to target movie (5 for Push, 1 for Nuke)
# Return:
#   Dictionary of Rating Attacks in format: (FictiveUser,Movie)=(Rating,Date)
#
def GenerateAttackTargetOnly(Percent, Frequency, Rating):
    # Dictionary of Ratings to be returned by the function
    # Key = (Fictive User, Movie)
    # Value = (Rating, Date)
    Ratings = {}

    # Number of target movies
    # (constant number as defined in the article)
    COUNT_TARGET_MOVIES = 32
    # If it is a Push Attack
    if (Rating == 5):
        GenerateSetTargetPush(COUNT_TARGET_MOVIES)
    # If it is a Nuke Attack
    elif (Rating == 1):
        GenerateSetTargetNuke(COUNT_TARGET_MOVIES)
    # List of appropriate target movies
    # Each movie is included multiple times
    # (depending on the Percent parameter as described in the article)
    AppropriateTargetMovies = list(TargetSet) * Percent
    # Set of chosen target movies to the user
    ChosenTargetMovies = set()
    # User Index
    CounterUsers = 1
    Counter = 1
    # While there is more appropriate target movies to divide for the users
    while len(AppropriateTargetMovies) > 0:
        # Choose random appropriate target movie from the list
        Index = random.randint(0, len(AppropriateTargetMovies) - 1)
        RandomTargetMovie = AppropriateTargetMovies[Index]
        # Restart Random on Deadlock
        Counter += 1
        if Counter == 10000: return GenerateAttackPopular(Percent, Frequency, Rating)
        # If the movie has not been already chosed by the user
        # then add it to the user movies set and remove the movie
        # from the appropriate list
        if RandomTargetMovie not in ChosenTargetMovies:
            # Add random target movie to the user target movies set
            ChosenTargetMovies.add(RandomTargetMovie)
            # Remove the random target movie from the appropriate list
            AppropriateTargetMovies.remove(RandomTargetMovie)
            # Add combined rating by the format (Fictive User, Movie) = (Rating, Date)
            Ratings[('F' + str(CounterUsers), RandomTargetMovie)] = (Rating, GenerateDate())
            # If the user chosen set is full then go to the next user
            if len(ChosenTargetMovies) == Frequency:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenTargetMovies = set()

                # Return Dictionary of Ratings: (Fictive User,Movie)=(Rating,Date)
    return Ratings


# =========================================================================================


# =========================================================================================
# Generate Average Attack Model
# Get:
#   1. Percent - Percentage of attack ratings from overall ratings of the Movie
#   2. Frequency - Amount of ratings per Attack User
#   3. Rating - Rating that will given to target movie (5 for Push, 1 for Nuke)
# Return:
#   Dictionary of Rating Attacks in format: (FictiveUser,Movie)=(Rating,Date)
#
def GenerateAttackAverage(Percent, Frequency, Rating):
    # Dictionary of Ratings to be returned by the function
    # Key = (Fictive User, Movie)
    # Value = (Rating, Date)
    Ratings = {}

    # Number of target movies
    # (constant number as defined in the article)
    COUNT_TARGET_MOVIES = 10
    # If it is a Push Attack
    if (Rating == 5):
        GenerateSetTargetPush(COUNT_TARGET_MOVIES)
    # If it is a Nuke Attack
    elif (Rating == 1):
        GenerateSetTargetNuke(COUNT_TARGET_MOVIES)
        # List of appropriate target movies
    # Each movie is included multiple times
    # (depending on the Percent parameter as described in the article)
    AppropriateTargetMovies = list(TargetSet) * Percent
    # Set of chosen target movies to the user
    ChosenTargetMovies = set()
    # User Index
    CounterUsers = 1
    Counter = 1
    # While there is more appropriate target movies to divide for the users
    while len(AppropriateTargetMovies) > 0:
        # Choose random appropriate target movie from the list
        Index = random.randint(0, len(AppropriateTargetMovies) - 1)
        RandomTargetMovie = AppropriateTargetMovies[Index]
        # Restart Random on Deadlock
        Counter += 1
        if Counter == 10000: return GenerateAttackPopular(Percent, Frequency, Rating)
        # If the movie has not been already chosed by the user
        # then add it to the user movies set and remove the movie
        # from the appropriate list
        if RandomTargetMovie not in ChosenTargetMovies:
            # Add random target movie to the user target movies set
            ChosenTargetMovies.add(RandomTargetMovie)
            # Remove the random target movie from the appropriate list
            AppropriateTargetMovies.remove(RandomTargetMovie)
            # Add combined rating by the format (Fictive User, Movie) = (Rating, Date)
            Ratings[('F' + str(CounterUsers), RandomTargetMovie)] = (Rating, GenerateDate())
            # If the user chosen set is full then go to the next user
            if len(ChosenTargetMovies) == COUNT_TARGET_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenTargetMovies = set()

    # Number of filler movies
    COUNT_FILLER_MOVIES = Frequency - COUNT_TARGET_MOVIES
    GenerateSetFiller(COUNT_FILLER_MOVIES)
    # List of appropriate filler movies
    AppropriateFillerMovies = list(FillerSet)
    # Number of Filler Movies for each user
    CounterRatings = COUNT_FILLER_MOVIES * (CounterUsers - 1)
    # Set of chosen target movies to the user
    ChosenFillerMovies = set()
    # User Index
    CounterUsers = 1
    # While there is more appropriate filler movies to divide for the users
    while CounterRatings > 0:
        # Choose random appropriate filler movie from the list
        Index = random.randint(0, len(AppropriateFillerMovies) - 1)
        RandomFillerMovie = AppropriateFillerMovies[Index]
        # If the movie has not been already chosed by the user
        # Add it to the user movies set
        if RandomFillerMovie not in ChosenFillerMovies:
            CounterRatings -= 1
            # Add random filler movie to the user target movies set
            ChosenFillerMovies.add(RandomFillerMovie)
            # Set Rating parameters in format:
            # (FictiveUser, FillerMovie) = (AverageRating,Date)
            FictiveUser = 'F' + str(CounterUsers)
            FillerMovie = RandomFillerMovie
            AverageRating = Movies[RandomFillerMovie][MOVIE_AVERAGE_RATING]
            Date = GenerateDate()
            # Add combined rating
            Ratings[(FictiveUser, FillerMovie)] = (AverageRating, Date)
            # If the user chosen set is full - then go to the next user
            if len(ChosenFillerMovies) == COUNT_FILLER_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenFillerMovies = set()

    # Return Dictionary of Ratings in format:
    # (Fictive User, Movie) = (Rating, Date)
    return Ratings


# =========================================================================================


# =========================================================================================
# Generate Random Attack Model
# Get:
#   1. Percent - Percentage of attack ratings from overall ratings of the Movie
#   2. Frequency - Amount of ratings per Attack User
#   3. Rating - Rating that will given to target movie (5 for Push, 1 for Nuke)
# Return:
#   Dictionary of Rating Attacks in format: (FictiveUser,Movie)=(Rating,Date)
#
def GenerateAttackRandom(Percent, Frequency, Rating):
    # Dictionary of Ratings to be returned by the function
    # Key = (Fictive User, Movie)
    # Value = (Rating, Date)
    Ratings = {}

    # Calc average ratings of all movies in the dataset
    SumRatingsMovies = 0.0
    for Movie in Movies.values():
        SumRatingsMovies += Movie[MOVIE_AVERAGE_RATING]
    # Set average rating of all movies in the dataset
    AverageRatingMovies = SumRatingsMovies / len(Movies)

    # Number of target movies
    # (constant number as defined in the article)
    COUNT_TARGET_MOVIES = 10
    # If it is a Push Attack
    if (Rating == 5):
        GenerateSetTargetPush(COUNT_TARGET_MOVIES)
    # If it is a Nuke Attack
    elif (Rating == 1):
        GenerateSetTargetNuke(COUNT_TARGET_MOVIES)
        # List of appropriate target movies
    # Each movie is included multiple times
    # (depending on the Percent parameter as described in the article)
    AppropriateTargetMovies = list(TargetSet) * Percent
    # Set of chosen target movies to the user
    ChosenTargetMovies = set()
    # User Index
    CounterUsers = 1
    Counter = 1
    # While there is more appropriate target movies to divide for the users
    while len(AppropriateTargetMovies) > 0:
        # Choose random appropriate target movie from the list
        Index = random.randint(0, len(AppropriateTargetMovies) - 1)
        RandomTargetMovie = AppropriateTargetMovies[Index]
        # Restart Random on Deadlock
        Counter += 1
        if Counter == 10000: return GenerateAttackPopular(Percent, Frequency, Rating)
        # If the movie has not been already chosed by the user
        # then add it to the user movies set and remove the movie
        # from the appropriate list
        if RandomTargetMovie not in ChosenTargetMovies:
            # Add random target movie to the user target movies set
            ChosenTargetMovies.add(RandomTargetMovie)
            # Remove the random target movie from the appropriate list
            AppropriateTargetMovies.remove(RandomTargetMovie)
            # Add combined rating by the format (Fictive User, Movie) = (Rating, Date)
            Ratings[('F' + str(CounterUsers), RandomTargetMovie)] = (Rating, GenerateDate())
            # If the user chosen set is full then go to the next user
            if len(ChosenTargetMovies) == COUNT_TARGET_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenTargetMovies = set()

    # Number of filler movies
    # (there is no filler movies as defined in the article)
    COUNT_FILLER_MOVIES = Frequency - COUNT_TARGET_MOVIES
    GenerateSetFiller(COUNT_FILLER_MOVIES)
    # List of appropriate filler movies
    AppropriateFillerMovies = list(FillerSet)
    # Number of Filler Movies for each user
    CounterRatings = COUNT_FILLER_MOVIES * (CounterUsers - 1)
    # Set of chosen Filler Movies to the user
    ChosenFillerMovies = set()
    # User Index
    CounterUsers = 1
    # While there is more appropriate filler movies to divide for the users
    while CounterRatings > 0:
        # Choose random appropriate filler movie from the list
        Index = random.randint(0, len(AppropriateFillerMovies) - 1)
        RandomFillerMovie = AppropriateFillerMovies[Index]
        # If the movie has not been already chosed by the user
        # Add it to the user movies set
        if RandomFillerMovie not in ChosenFillerMovies:
            CounterRatings -= 1
            # Add random filler movie to the user target movies set
            ChosenFillerMovies.add(RandomFillerMovie)
            # Set Rating parameters in format:
            # (FictiveUser, FillerMovie) = (AverageRating,Date)
            FictiveUser = 'F' + str(CounterUsers)
            FillerMovie = RandomFillerMovie
            AverageRating = AverageRatingMovies
            Date = GenerateDate()
            # Add combined rating
            Ratings[(FictiveUser, FillerMovie)] = (AverageRating, Date)
            # If the user chosen set is full - then go to the next user
            if len(ChosenFillerMovies) == COUNT_FILLER_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenFillerMovies = set()

    # Return Dictionary of Ratings in format:
    # (Fictive User, Movie) = (Rating, Date)
    return Ratings


# =========================================================================================


# =========================================================================================
# Generate Love/Hate Attack Model
#
# Get:
#   1. Percent - Percentage of attack ratings from overall ratings of the Movie
#   2. Frequency - Amount of ratings per Attack User
#   3. Rating - Rating that will given to target movie (5 for Push, 1 for Nuke)
#   4. RatingFiller - Rating that will given to filler movie (1 for Push, 5 for Nuke)
# Return:
#   Dictionary of Rating Attacks in format: (FictiveUser,Movie)=(Rating,Date)
#
def GenerateAttackLoveHate(Percent, Frequency, RatingTarget, RatingFiller):
    # Dictionary of Ratings to be returned by the function
    # Key = (Fictive User, Movie)
    # Value = (Rating, Date)
    Ratings = {}

    # Number of target movies
    # (constant number as defined in the article)
    COUNT_TARGET_MOVIES = 10
    # If it is a Push Attack
    if (RatingTarget == 5):
        GenerateSetTargetPush(COUNT_TARGET_MOVIES)
    # If it is a Nuke Attack
    elif (RatingTarget == 1):
        GenerateSetTargetNuke(COUNT_TARGET_MOVIES)
        # List of appropriate target movies
    # Each movie is included multiple times
    # (depending on the Percent parameter as described in the article)
    AppropriateTargetMovies = list(TargetSet) * Percent
    # Set of chosen target movies to the user
    ChosenTargetMovies = set()
    # User Index
    CounterUsers = 1
    Counter = 1
    # While there is more appropriate target movies to divide for the users
    while len(AppropriateTargetMovies) > 0:
        # Choose random appropriate target movie from the list
        Index = random.randint(0, len(AppropriateTargetMovies) - 1)
        RandomTargetMovie = AppropriateTargetMovies[Index]
        # Restart Random on Deadlock
        Counter += 1
        if Counter == 10000: return GenerateAttackPopular(Percent, Frequency, Rating)
        # If the movie has not been already chosed by the user
        # then add it to the user movies set and remove the movie
        # from the appropriate list
        if RandomTargetMovie not in ChosenTargetMovies:
            # Add random target movie to the user target movies set
            ChosenTargetMovies.add(RandomTargetMovie)
            # Remove the random target movie from the appropriate list
            AppropriateTargetMovies.remove(RandomTargetMovie)
            # Add combined rating by the format (Fictive User, Movie) = (Rating, Date)
            Ratings[('F' + str(CounterUsers), RandomTargetMovie)] = (RatingTarget, GenerateDate())
            # If the user chosen set is full then go to the next user
            if len(ChosenTargetMovies) == COUNT_TARGET_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenTargetMovies = set()

    # Number of filler movies
    # (there is no filler movies as defined in the article)
    COUNT_FILLER_MOVIES = Frequency - COUNT_TARGET_MOVIES
    GenerateSetFiller(COUNT_FILLER_MOVIES)
    # List of appropriate filler movies
    AppropriateFillerMovies = list(FillerSet)
    # Number of Filler Movies for each user
    CounterRatings = COUNT_FILLER_MOVIES * (CounterUsers - 1)
    # Set of chosen Filler Movies to the user
    ChosenFillerMovies = set()
    # User Index
    CounterUsers = 1
    # While there is more appropriate filler movies to divide for the users
    while CounterRatings > 0:
        # Choose random appropriate filler movie from the list
        Index = random.randint(0, len(AppropriateFillerMovies) - 1)
        RandomFillerMovie = AppropriateFillerMovies[Index]
        # If the movie has not been already chosed by the user
        # Add it to the user movies set
        if RandomFillerMovie not in ChosenFillerMovies:
            CounterRatings -= 1
            # Add random filler movie to the user target movies set
            ChosenFillerMovies.add(RandomFillerMovie)
            # Set Rating parameters in format:
            # (FictiveUser, FillerMovie) = (RatingFiller,Date)
            FictiveUser = 'F' + str(CounterUsers)
            FillerMovie = RandomFillerMovie
            Date = GenerateDate()
            # Add combined rating
            Ratings[(FictiveUser, FillerMovie)] = (RatingFiller, Date)
            # If the user chosen set is full - then go to the next user
            if len(ChosenFillerMovies) == COUNT_FILLER_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenFillerMovies = set()

    # Return Dictionary of Ratings in format:
    # (Fictive User, Movie) = (Rating, Date)
    return Ratings


# =========================================================================================


# =========================================================================================
# Generate Popular Attack Model
#
# Get:
#   1. Percent - Percentage of attack ratings from overall ratings of the Movie
#   2. Frequency - Amount of ratings per Attack User
#   3. Rating - Rating that will given to target movie (5 for Push, 1 for Nuke)
# Return:
#   Dictionary of Rating Attacks in format: (FictiveUser,Movie)=(Rating,Date)
#
def GenerateAttackPopular(Percent, Frequency, Rating):
    # Dictionary of Ratings to be returned by the function
    # Key = (Fictive User, Movie)
    # Value = (Rating, Date)
    Ratings = {}

    # Number of target movies
    # (constant number as defined in the article)
    COUNT_TARGET_MOVIES = 10
    # If it is a Push Attack
    if (Rating == 5):
        GenerateSetTargetPush(COUNT_TARGET_MOVIES)
    # If it is a Nuke Attack
    elif (Rating == 1):
        GenerateSetTargetNuke(COUNT_TARGET_MOVIES)
        # List of appropriate target movies
    # Each movie is included multiple times
    # (depending on the Percent parameter as described in the article)
    AppropriateTargetMovies = list(TargetSet) * Percent
    # Set of chosen target movies to the user
    ChosenTargetMovies = set()
    # User Index
    CounterUsers = 1
    Counter = 1
    # While there is more appropriate target movies to divide for the users
    while len(AppropriateTargetMovies) > 0:
        # Choose random appropriate target movie from the list
        Index = random.randint(0, len(AppropriateTargetMovies) - 1)
        RandomTargetMovie = AppropriateTargetMovies[Index]
        # Restart Random on Deadlock
        Counter += 1
        if Counter == 10000: return GenerateAttackPopular(Percent, Frequency, Rating)
        # If the movie has not been already chosed by the user
        # then add it to the user movies set and remove the movie
        # from the appropriate list
        if RandomTargetMovie not in ChosenTargetMovies:
            # Add random target movie to the user target movies set
            ChosenTargetMovies.add(RandomTargetMovie)
            # Remove the random target movie from the appropriate list
            AppropriateTargetMovies.remove(RandomTargetMovie)
            # Add combined rating by the format (Fictive User, Movie) = (Rating, Date)
            Ratings[('F' + str(CounterUsers), RandomTargetMovie)] = (Rating, GenerateDate())
            # If the user chosen set is full then go to the next user
            if len(ChosenTargetMovies) == COUNT_TARGET_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenTargetMovies = set()

    # Amount of selected movies
    # (constant number defined after empirically experiments)
    COUNT_SELECTED_MOVIES = 10
    # If it is a Push Attack
    if (Rating == 5):
        GenerateSetSelectedPush(COUNT_SELECTED_MOVIES)
    # If it is a Nuke Attack
    elif (Rating == 1):
        GenerateSetSelectedNuke(COUNT_SELECTED_MOVIES)
    # List of appropriate Selected Movies
    AppropriateSelectedMovies = list(SelectedSet)
    # Amount of Selected Movies for each user
    CounterRatings = COUNT_SELECTED_MOVIES * (CounterUsers - 1)
    # Set of chosen Selected Movies to the user
    ChosenSelectedMovies = set()
    # User Index
    CounterUsers = 1
    # While there is more appropriate Selected Movies to divide for the users
    while CounterRatings > 0:
        # Choose random appropriate Selected Movie from the list
        Index = random.randint(0, len(AppropriateSelectedMovies) - 1)
        RandomSelectedMovie = AppropriateSelectedMovies[Index]
        # If the movie has not been already chosed by the user
        # Add it to the user movies set
        if RandomSelectedMovie not in ChosenSelectedMovies:
            CounterRatings -= 1
            # Add random Selected Movie to the user movies set
            ChosenSelectedMovies.add(RandomSelectedMovie)
            # Set Rating parameters in format:
            # (FictiveUser, SelectedMovie) = (Rating,Date)
            FictiveUser = 'F' + str(CounterUsers)
            SelectedMovie = RandomSelectedMovie
            Date = GenerateDate()
            # Add combined rating
            Ratings[(FictiveUser, SelectedMovie)] = (Rating, Date)
            # If the user chosen set is full - then go to the next user
            if len(ChosenSelectedMovies) == COUNT_SELECTED_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenSelectedMovies = set()

    # Amount of filler movies
    COUNT_FILLER_MOVIES = Frequency - COUNT_TARGET_MOVIES - COUNT_SELECTED_MOVIES
    GenerateSetFiller(COUNT_FILLER_MOVIES)
    # List of appropriate filler movies
    AppropriateFillerMovies = list(FillerSet)
    # Number of Filler Movies for each user
    CounterRatings = COUNT_FILLER_MOVIES * (CounterUsers - 1)
    # Set of chosen target movies to the user
    ChosenFillerMovies = set()
    # User Index
    CounterUsers = 1
    # While there is more appropriate filler movies to divide for the users
    while CounterRatings > 0:
        # Choose random appropriate filler movie from the list
        Index = random.randint(0, len(AppropriateFillerMovies) - 1)
        RandomFillerMovie = AppropriateFillerMovies[Index]
        # If the movie has not been already chosed by the user
        # Add it to the user movies set
        if RandomFillerMovie not in ChosenFillerMovies:
            CounterRatings -= 1
            # Add random filler movie to the user target movies set
            ChosenFillerMovies.add(RandomFillerMovie)
            # Set Rating parameters in format:
            # (FictiveUser, FillerMovie) = (RandomRating,Date)
            FictiveUser = 'F' + str(CounterUsers)
            FillerMovie = RandomFillerMovie
            RandomRating = random.randint(1, 5)
            Date = GenerateDate()
            # Add combined rating
            Ratings[(FictiveUser, FillerMovie)] = (RandomRating, Date)
            # If the user chosen set is full - then go to the next user
            if len(ChosenFillerMovies) == COUNT_FILLER_MOVIES:
                # Go to the next user
                CounterUsers += 1
                # Initialize the user chosen target movies set
                ChosenFillerMovies = set()

                # Return Dictionary of Ratings in format:
    # (Fictive User, Movie) = (Rating, Date)
    return Ratings


# =========================================================================================


# =========================================================================================
# Function writes ratings dictionary to the CSV file
#
# Get:
#   1. Ratings - Dictionary in format: (FictiveUser,Movie)=(Rating,Date)
#   2. Path - File Path of CSV file
#
def RatingsToCsv(Ratings, Path):
    f = open(Path, 'w')

    for DataRating in Ratings.keys():
        User = DataRating[0]
        Movie = DataRating[1]
        Rating = Ratings[DataRating][0]
        Date = Ratings[DataRating][1]
        Line = '{},{},{},{}'.format(User, Movie, Rating, Date)
        f.write(Line + '\n')

    f.close()


# =========================================================================================


# =========================================================================================
# Create CSV files with Rating Attacks
#
# For every Frequency and Percent parameters that described in the article, the
# function executes all experiments of 10 Rating Attack Models (5 for Push, 5 for Nuke)
# and stores the results in CSV files in format: (FictiveUser,Movie)=(Rating,Date)
#
def CreateRatingAttackFile():
    # Load Movies data
    for Movie in movies_user_rating.keys():
        # Add new movie to Movies
        if Movie not in Movies:
            # [ count ratings, sum ratings, average rating ]
            Movies[Movie] = [0, 0.0, 0.0]
        # Update Rating
        Movies[Movie][MOVIE_COUNT_RATINGS] += 1
        Movies[Movie][MOVIE_SUM_RATINGS] += float(rating)

    # Set average rating for each Movie
    for Movie in Movies.keys():
        Movies[Movie][MOVIE_AVERAGE_RATING] = Movies[Movie][MOVIE_SUM_RATINGS] / Movies[Movie][MOVIE_COUNT_RATINGS]

    # Create Target Only Attacks files
    # (Frequency and Percent parameters defined as in the article)
    for Frequency in [2, 32]:
        for Percent in [5, 10, 15, 20, 25, 30]:
            # Create Target Only Push Attacks files
            Ratings = GenerateAttackTargetOnly(Percent, Frequency, 5)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Target_Push_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Target Only Nuke Attacks files
            Ratings = GenerateAttackTargetOnly(Percent, Frequency, 1)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Target_Nuke_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)

    # Create other Attacks files
    # (Frequency and Percent parameters defined as in the article)
    for Frequency in [50, 100]:
        for Percent in [5, 10, 15, 20, 25, 30]:
            # Create Random Push Attacks files
            Ratings = GenerateAttackRandom(Percent, Frequency, 5)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Random_Push_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Random Nuke Attacks files
            Ratings = GenerateAttackRandom(Percent, Frequency, 1)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Random_Nuke_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Average Push Attacks files
            Ratings = GenerateAttackAverage(Percent, Frequency, 5)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Average_Push_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Average Nuke Attacks files
            Ratings = GenerateAttackAverage(Percent, Frequency, 1)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Average_Nuke_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Popular Push Attacks files
            Ratings = GenerateAttackPopular(Percent, Frequency, 5)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Popular_Push_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Popular Nuke Attacks files
            Ratings = GenerateAttackPopular(Percent, Frequency, 1)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\Popular_Nuke_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Love/Hate Push Attacks files
            Ratings = GenerateAttackLoveHate(Percent, Frequency, 5, 1)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\LoveHate_Push_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)
            # Create Love/Hate Nuke Attacks files
            Ratings = GenerateAttackLoveHate(Percent, Frequency, 1, 5)
            Path = r'G:\Study\Recommend Systems\Main Article\RA\LoveHate_Nuke_' + str(Frequency) + '_' + str(
                Percent) + '.csv'
            RatingsToCsv(Ratings, Path)


# =========================================================================================


# Dictionary of Movies
# Key = Movie Id
# Value = List [Count ratings, Sum ratings, Average rating]
Movies = {}
# Indexes in Movie's parameters list
MOVIE_COUNT_RATINGS = 0
MOVIE_SUM_RATINGS = 1
MOVIE_AVERAGE_RATING = 2

# Set of Movies chosen to be a target movies
TargetSet = set()
# Set of Movies chosed to be a selected movies
SelectedSet = set()
# Set of Movies chosed to be a filler movies
FillerSet = set()













