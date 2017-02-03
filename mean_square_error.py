
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


RatingTable = Table()
f = open('./data/u1.test', 'r')
for l in f.readlines():
    l = l.split('\t')
    userid = int(l[0])
    movieid = int(l[1])
    rating = float(l[2])
    RatingTable.set(userid, movieid, rating)


PredTable = Table()
f = open('./data/u1.test.Prediction', 'r')
for l in f.readlines():
    l = l.split('\t')
    userid = int(l[0])
    movieid = int(l[1])
    rating = float(l[2])
    PredTable.set(userid, movieid, rating)

n = 0
res = 0

# For Python 2, use RatingTable.iteritems()
for key,rating in RatingTable.items():
    pred_rating = PredTable.read(key[0], key[1])

    res += (pred_rating - rating) ** 2
    n = n + 1


res = res/float(n)

print("Mean Square Error: {:0.2f}".format(res))
