
DESCRIPTIONS OF DATA FILES
==============================================

u.item     -- Information about the movies; this is a list of
              movie id | movie title | release date | video release date |
              IMDb URL | unknown | Action | Adventure | Animation |
              Children's | Comedy | Crime | Documentary | Drama | Fantasy |
              Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
              Thriller | War | Western |
              The last 19 fields are the genres, a 1 indicates the movie
              is of that genre, a 0 indicates it is not; movies can be in
              several genres at once.
              The movie ids are the ones used in the data set.


u.user     -- Demographic information about the users; this is a list of
              user id | age | gender | occupation | zip code
              The user ids are the ones used in the data set.


u1.base    -- The data sets u1.base and u1.test through u5.base and u5.test
u1.test       are 80%/20% splits of the data into training and test data.
u2.base       Each of u1, ..., u5 have disjoint test sets; this is for
u2.test       5 fold cross validation (where you repeat your experiment
u3.base       with each training and test set and average the results).
u3.test       
u4.base
u4.test
u5.base
u5.test
