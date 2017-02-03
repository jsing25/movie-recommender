import math
import time

class Table(dict):
    def __init__(self):
        self.value_indices = {}
    
    def set(self, i, j, v):
        self[(i, j)] = v
        if i in self.value_indices:
            self.value_indices[i].add(j)
        else:
            self.value_indices[i] = set([j])
        
    def read(self, i, j):
        return self.get((i, j), None)
    
    def has_values(self, i):
        idx = self.value_indices.get(i, None)
        return idx

    def get_users(self):
        res = []
        for key in self.value_indices:
            res.append(key)

        return res

    def get_values(self, i):
        v = self.has_values(i)
        res = set()

        if v is None:
            return res

        for j in v:
            res.add(self.read(i, j))

        return res

    def get_intersection_values(self, i, j):
        res1 = []
        res2 = []

        v1 = self.has_values(i)
        v2 = self.has_values(j)

        if v1 is None or v2 is None:
            return (res1, res2)

        overlap = v1.intersection(v2)

        for value in overlap:
            res1.append(self.read(i, value))
            res2.append(self.read(j, value))

        return (res1, res2)


# Get user similarity using Pearson correlation
def get_sim(a, b):
    # Check if this value has been
    # previously calculated.
    sim = SimTable.read(a, b)

    if sim is None:
        sim = SimTable.read(b, a)
    else:
        # Return the value if it has already
        # been calculated.
        return sim

    # Find the intersection of user a and user b
    # ratings and get those ratings.
    a_b_values = T.get_intersection_values(a, b)
    a_ratings = a_b_values[0]
    b_ratings = a_b_values[1]

    n = len(a_ratings)

    # Avoid division by 0.
    if n == 0:
        SimTable.set(a, b, 0)
        return 0

    # Calculate the mean for user a and user b.
    a_mean = sum(a_ratings)/n
    b_mean = sum(b_ratings)/n

    a_std = []
    b_std = []
    square_sum_a = 0
    square_sum_b = 0
    num = 0

    # Calculate the Pearson correlation.
    for i in range(n):
        a_std.append(a_ratings[i] - a_mean)
        b_std.append(b_ratings[i] - b_mean)
        square_sum_a += (a_std[i] * a_std[i])
        square_sum_b += (b_std[i] * b_std[i])
        num += a_std[i] * b_std[i]

    den = math.sqrt(square_sum_a * square_sum_b)

    # Avoid divison by 0.
    if den == 0:
        SimTable.set(a, b, 1)
        return 1

    res = num / den

    # Store the value.
    SimTable.set(a, b, res)
    
    return res
    

# Predict a user rating for user a on item p.
def predict(a, p):
    # Get the set of similar users.
    N = get_similar_users(a, p)

    # Get all the movie ratings made by user a.
    a_ratings = T.get_values(a)

    if len(a_ratings) == 0:
        return 0

    # Calculate the mean for user a.
    a_mean = sum(a_ratings)/len(a_ratings)

    res = []

    # Loop through the set of similar users.
    for user in N:

        # Get the ratings for a given user
        # and calculate the mean.
        b_ratings = T.get_values(user[0])
        b_mean = sum(b_ratings)/len(b_ratings)

        # Use the previously calculated
        # sim score for the user.
        sim = user[1]

        # Find the user rating for the 
        # movie we are trying to predict.
        b_rating_p = T.read(user[0], p)

        # Avoid division by 0.
        if sim == 0 or b_rating_p is None:
            res.append(0)
        else:
            res.append((sim * (b_rating_p - b_mean) / sim))

    # Avoid division by 0.
    if len(res) == 0:
        return a_mean

    # Calculate the predicted rating.
    pred = a_mean + sum(res)/len(res)

    # Check that the rating is within
    # the correct bounds.
    if pred > 5.0:
        return 5.0
    elif pred < 0.0:
        return 0.0
    else:
        return pred


# Find up to 3 users and calculate their
# similarity scores.
def get_similar_users(a, movieid):
    # Get all the users
    users = T.get_users()
    res = []

    # Loop through the users and get the sim score
    # for up to 3 similar users (where sim score > .5)
    for user in users:
        if user == a:
            continue

        if T.read(user, movieid) is not None:
            sim = get_sim(a, user)
            if sim > 0.5:
                res.append((user, sim))

        # Limit to 3 users for efficiency
        if len(res) == 3:
            break

    return res


if __name__ == "__main__":
    start_time = time.time()

    T = Table()
    SimTable = Table()
    f = open('./data/u5.base', 'r')
    for l in f.readlines():
        l = l.split('\t')
        userid = int(l[0])
        movieid = int(l[1])
        rating = float(l[2])
        T.set(userid, movieid, rating)
    f.close()

    users = []
    movies = []

    test_file = open('./data/utest', 'r')
    for l in test_file.readlines():
        l = l.split('\t')
        users.append(int(l[0]))
        movies.append(int(l[1]))
    test_file.close()

    res_file = open('./data/utest.Prediction', 'w')
    for i in range(len(users)):
        res_file.write('{} \t {} \t {:.2f}\n'.format(users[i], movies[i], predict(users[i], movies[i])))

    res_file.close()

    print("runtime: {0:.2f} sec".format(time.time() - start_time))
