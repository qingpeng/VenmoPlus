def distance(a,b):
    if a in r.smembers(b) or b in r.smembers(a):
        return 1
    elif r.smembers(a).isdisjoint(r.smembers(b)) !=True:
        return 2
    else:
         
        second_degree = set()
        for s in r.smembers(a):
            second_degree = second_degree.union(r.smembers(s))
        print second_degree
        print r.smembers(b)
        print second_degree & r.smembers(b)
        if second_degree.isdisjoint(r.smembers(b)):
            return 0
        else:
            return 3

from collections import Counter

def friend_recommend(a):
    
    second_degree = []
    for s in r.smembers(a):
        second_degree.extend(list(r.smembers(s)))
    
    return Counter(second_degree)

