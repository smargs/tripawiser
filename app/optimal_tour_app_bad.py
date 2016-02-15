
 

############################################################
## all inputs required #####################################
# user_weights, attraction weights, attraction_review_num ##
# dist matrix of distance between attractions 
# maxlen = maximum time that user has


import numpy as np
import itertools

def rating_score(num):
    if float(num) == 5.0:
        ans1 = 5;
    if float(num) == 4.5:
        ans1 = 4.7;
    if float(num) == 4.0:
        ans1 = 4.2;
    if float(num) <= 3.5:
        ans1 = 2;
    return ans1

def att_prize(u_f,at_f,review_num,rating):
    return np.dot(u_f,at_f)*(review_num)*rating_score(rating)
######################################################
## TSP DP to calculate shortest paths which can be ###
## finished within time maxlen #######################
## then choosing between the paths based on 


def optimal_tour_app(maxlen,dist,attraction_weights,user_weights,attraction_review_num,fin_attraction_ratings):
 
#########################################################
## this DOES INCLUDE attraction 0 while finding tours ###
## maybe this attraction can be specified or the code can 
## be modified to include different starting points #####
## the latter will increase complexity of code ##########
 
    def tsp_dp_mod(dist,maxlen):
        all_tours = []; all_tours_len = [];
        p0 = 0; flag = 0;
        #initial value - just distance from p0 to every other attraction + keep the track of edges
        S1 = {(frozenset([p0, idx+1]), idx+1): (dist, [p0,idx+1]) for idx,dist in enumerate(dist[p0][1:])}
        cnt = len(dist)
        flag = 0
        for m in range(2, cnt):
            if flag == 0:
                S2 = {}
                for S in [frozenset(C) | {p0} for C in itertools.combinations(range(1, cnt), m)]:
                    for j in S - {p0}:
                        S2[(S, j)] = min( [(S1[(S-{j},k)][p0] + dist[k][j], S1[(S-{j},k)][1] + [j]) for k in S if k != p0 and k!=j])   
                S1 = S2
                dum = min([(S2[d][p0] + dist[p0][d[1]], S2[d][1]) for d in iter(S1)])
                
                if (dum[0] > maxlen) & (flag == 0):
                    flag = 1
                else:
                    all_tours_len.append(dum[0]); all_tours.append(dum[1])
                    print 'min tour of size', m +1 , 'starting at',p0,'is' ,dum[1] ,'and of length', dum[0]
                    
        return all_tours, all_tours_len
    
    def prize_winner(user_weights,attraction_weights,all_tours,all_tours_len,rating_score,attraction_review_num):
        prize = np.zeros((len(all_tours_len),1))
        for i,j in enumerate(all_tours_len):
            prize[i] = 0
            for s,k in enumerate(all_tours[i]):
                at_f = attraction_weights[k,:]
                u_f = user_weights;   
                prize[i] = prize[i] + att_prize(u_f,at_f,attraction_review_num[k][0],fin_attraction_ratings[k][0])         
                print prize, all_tours[i]
        # want to maximize prize
        x = np.argmax(prize)                              
        mytour = all_tours[x]
        mytourlen = all_tours_len[x]
        return mytour,mytourlen
    maxh = 3.5;
    if maxlen > maxh*60:
        maxlen1 = maxh*60;  
    else:
        maxlen1 = maxlen
    print 'maxlen1 is ', maxlen1
    all_tours1,all_tours_len1 =  tsp_dp_mod(dist,maxlen1)
    mytour1,mytourlen1 = prize_winner(user_weights,attraction_weights,all_tours1,all_tours_len1,rating_score,attraction_review_num)
    print 'first tour is' ,mytour1
    maxlen2 = maxlen-mytourlen1
    distnow = np.zeros((len(dist),len(dist)));
    for i in range(len(dist)): 
        for k in range(len(dist)):
            if (i in mytour1) | (k in mytour1):
                distnow[i,k] = 1000000; distnow[k,i] = 1000000;
            else: 
                distnow[i,k] = dist[i,k]; distnow[k,i] = dist[k,i];
    
    for k in range(len(dist)):
        distnow[0,k] = dist[mytour1[-1],k];
        distnow[k,0] = dist[k,mytour1[-1]];
    print 'maxlen2 is ', maxlen2
    all_tours2,all_tours_len2 =  tsp_dp_mod(distnow,maxlen2)
    if len(all_tours2) == 0:
        mytour = mytour1
        print 'final tour is is' ,mytour
    else:
        mytour2,mytourlen2 = prize_winner(user_weights,attraction_weights,all_tours2,all_tours_len2,rating_score,attraction_review_num)
        print 'second tour is' ,mytour2
        mytour = mytour1 + mytour2[1::]
        print 'final tour is' ,mytour

    
    # calculating the final TSP over both tours
    at_dict = {}; at_dict_rev = {};
    disttsp = np.zeros((len(mytour),len(mytour)));
    for i,j in enumerate(mytour):
        at_dict[i] = j; at_dict_rev[j] = i
    for i in range(len(mytour)):
        for j in range(len(mytour)):
            disttsp[i,j] = dist[at_dict[i],at_dict[j]]
    
    mytourshort = tsp_dp_mod(disttsp,100000)
    mytourshort = mytourshort[0][-1]
    x = [];
    for i in range(len(mytourshort)):
        x.append(at_dict[mytourshort[i]])
    
    mytour = x     
    print 'and x is', x
    mytour_u = []; done = [];
    for i,j in enumerate(mytour):
        if j not in done:
            done.append(j); mytour_u.append(j);
    mytour = mytour_u
    return mytour

    # ideas on including popularity score, off beaten paths
    #def popularity(rev_count):
    #    beta_vec = [5000,1000,500,200,50]
    #    popularity = len(beta_vec)-1
    #    for i,j in enumerate(beta_vec):
    #        if rev_count < j:
    #            popularity = len(beta_vec)-1-i
    #    return popularity
    
    # one way of inserting popularity of attraction
    #
    #def off_beaten_path(beta):
    #    # popularity score of attractions
    #    # beta = 0 means that I wan't only the most popular attractions
    #    beta_vec = [5000,1000,500,200,50]
    #    return beta_vec[beta]
    #
    #prize = np.zeros((len(all_tours_len),1))
    #for i,j in enumerate(all_tours_len):
    #    if max(attraction_review_num[all_tours[i],:])[0] < off_beaten_path(beta):
    #        # satisfies how popular or not the user wants his destinations to be
    #        prize[i] = 0
    #        for s,k in enumerate(all_tours[i]):
    #            at_f = attraction_weights[k,:]
    #            u_f = user_weights;  
    #            prize[i] = prize[i] + np.dot(u_f,at_f)
     
    # one way of inserting popularity of attraction   
    
    
    
    
######################################################
## sample input generator ############################
#from numpy import random
#import numpy as np
#n = 20;   
#dist = np.zeros((n,n))
#for i in range(n):
#    for j in range(n):
#        dist[i][j] = np.zeros((n,n))
#maxlen = 7;
## m features associated with each attraction
## each row  represents one attraction
#m = 3; attraction_weights = random.rand(n,m)
#user_weights = random.rand(1,m)[0]
#attraction_review_num = 5000*random.rand(n,1)

#print optimal_tour(maxlen,dist,attraction_weights,user_weights,attraction_review_num)



