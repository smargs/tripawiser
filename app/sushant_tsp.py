 
import itertools
import numpy as np


def tsp_prize(dist,maxlen,prize):
    n = len(dist); prize_dict = {}; dist_dict = {}; tour_dict = {};
    best_tour = []; best_tour_len = 0;
    best_tour_prize = 0;
    for i in range(2,n+1):
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

n = 10;  prize = [1]*n;
maxlen = 50;

points = np.random.rand(n,2); 
#points = np.array([[2.,0.],[0.,1.],[1.,0.],[1.,2.]])
dist = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        dist[i][j] = sum((points[i]-points[j])**2)**0.5


for i in range(n):
    dist[i,i] = 0;
    
best_tour, minlen= tsp_prize(dist,maxlen,prize)

import matplotlib.pyplot as plt
fin_points = points[best_tour,:];
for i in range(len(fin_points)):
    if i < len(fin_points)-1:
        a = fin_points[i][0]; b = fin_points[i][1]
        c = fin_points[i+1][0]; d = fin_points[i+1][1]
    plt.plot([a,c],[b,d])
    
plt.show()  
    
    
    
    
    
    