The domain of this git repository is recommendation system attacks.
Attack file are given, reputation adjustment algorithms and there comparision methods are implemented.

In particular different attack files are given in "attack files" folder.
Each attack type has different number of inserted attackers (father folder).
For example "Average Nuke 100" means the attack is "Average Nuke" and there are 100 attackers inserted.
Under each attack father folder there are several files. Each file contains a different the percentage of attacked ratings out of the total number of ratings per movie.
The attack files were generated using the RA.py, please have a look in it's documentation for more details.
For more information please see the RA.py file and the "Improving the True-Reputation Algorithm by Age Parameters.pdf" article.
To create the attack files please run "CreateRatingAttackFiles" function in RA.py file

The reputation adjustment algorithm that were implemented are arithmetic mean, true reputation, true reputation improved.
A reputation algorithm gets all user item ratings and returns a reputation vector (algorithm depended).
"Arithmetic Mean" returns a reputation vector that contains for each movie its arithmetic mean.
"True Reputation" returns a reputation vector that contains for each movie its reputation based on the "true reputation" algorithm discussed in "Can You Trust Online Ratings.pdf" paper.
"Improved True Reputation" returns a reputation vector that contains for each movie its reputation based on the "improved true reputation" algorithm discussed in "Improving the True-Reputation Algorithm by Age Parameters.pdf" paper.
The algorithms are implemented in the ReputationAlgorithms.py file.

Different comparision methods are implemented.
Evaluation of the effectiveness of each new improvement in the "improved true reputation" algorithm (user age, movie age, const cutoff, percentile cutoff) using comparision plots.
Comparision and plot between "Improved True Reputation" to "Arithmetic Mean" and "True Reputation" for different attack types.
Implementation and more details can be found in  RunAttacks.py file.
Results can be found in the "Improving the True-Reputation Algorithm by Age Parameters.pdf" paper.

Finally the Main.py is an example python file that performs an attack and compares different reputation adjustment algorithms.
The algorithms are implemented in the Main.py file.