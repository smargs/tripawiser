
 

############################################################
## all inputs required #####################################
# user_weights, attraction weights, attraction_review_num ##
# dist matrix of distance between attractions 
# maxlen = maximum time that user has


import numpy as np
import itertools


def optimal_tour_app(maxlen,dist,attraction_weights,user_weights,attraction_review_num,fin_attraction_ratings,prize):
    def tsp_prize(dist,maxlen,prize):
        max_attractions = 7;
        n = len(dist); prize_dict = {}; dist_dict = {}; tour_dict = {};
        best_tour = []; best_tour_len = 0;
        best_tour_prize = 0;
        for i in range(2,min(max_attractions,n)+1):
            print 'Sets of size ',i
            minlen = np.inf
            for s in itertools.combinations(range(1,n),i-1):
                s = frozenset(s);
                if len(s) == 1:
                    (j,) = s
                    dist_dict[(s,j)] = dist[0,j];
                    prize_dict[s] = prize[j];
                    tour_dict[(s,j)] = [0,j];
                    minlen = min(minlen, dist_dict[(s,j)])
                else:
                    for j in s: 
                        prize_dict[s] = prize_dict[s-{j}] + prize[j];
                        minval = np.inf; min_k = -1;
                        for k in s-{j}:
                            temp_val = dist_dict[(s-{j}),k] + dist[k,j]
                            if temp_val < minval:
                                minval = temp_val; 
                                min_k = k;
                        dist_dict[(s,j)] = minval; 
                        tour_dict[(s,j)] = tour_dict[(s-{j},min_k)] + [j] 
                        if (minval < maxlen) & (prize_dict[s]>best_tour_prize):
                            best_tour = tour_dict[(s,j)]
                            best_tour_prize = prize_dict[s]
                            best_tour_len = minval
                        minlen = min(minval,minlen);
            if minlen > maxlen:
                break; 
        
        return best_tour, best_tour_len
 
    
    best_tour, best_tour_len = tsp_prize(dist,maxlen,prize)
    return best_tour,best_tour_len

 