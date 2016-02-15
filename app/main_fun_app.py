##################################################
### tour builder #################################
import json
import urllib2
import urllib
import numpy as np

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
    return np.dot(u_f,at_f)*((review_num)**0.5)*rating_score(rating)

def get_latlon(address): 
    encodedAddress = urllib.quote_plus(address)
    data = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=" + encodedAddress + '&sensor=false').read()
    location = json.loads(data)['results'][0]['geometry']['location']
    lat = location['lat']
    lon = location['lng']
    return lat, lon 

def main_fun_app(user_features,maxtime,home_latlon):

##################################################
### building the distance matrix #################
    import math
    import pickle
    import numpy as np
    from optimal_tour_app import optimal_tour_app
 
    ##################################################
    ### loading all data #############################
    
    #homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
    #homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
    #homeurl = 'app/static/data/'
    homeurl = '/home/smargs/app/data/'
    with open(homeurl+'all_attractions_new.pickle') as f:
        attraction_names,attraction_urls  = pickle.load(f) 
        
    #with open(homeurl+'flickrimages.pickle') as f:
    #    photourl_dictionary,owner_dictionary = pickle.load(f) 
 
    with open(homeurl+'all_attractions_info_new.pickle') as f:
        attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description,categories_key,categories_dict,catnames = pickle.load(f) 
    attraction_latlon['Golden_Gate_Bridge'] = (37.807715, -122.475164)
    with open(homeurl+'attractions_categories_new.pickle') as f:
        catnames,categories_dict = pickle.load(f) 
     
    
    #homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
    #with open(homeurl+'all_attractions_new.pickle') as f:
    #    attraction_names,attraction_urls  = pickle.load(f) 
    
    #with open(homeurl+'all_attractions_info_new.pickle') as f:
    #    attraction_info,attraction_title,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count = pickle.load(f) 
        
    
    ###################################################
    ## including the visit times ######################
    ## setting all to 60 minutes right now ############
    ## will have to be extracted eventually ###########
    visit_times = {}
    for i,j in enumerate(attraction_names):
        visit_times[j] = attraction_time[j];
        if ('tours' in j) | ('Tours' in j) | ('tour' in j) | ('Tour' in j) | ('museum' in j) | ('Museum' in j):
            visit_times[j] = 90;
        elif  attraction_time[j] == 30:
            visit_times[j] = 45;
        
            
    ###################################################
    ### user input ####################################    
    maxtime = float(maxtime)*60 # maxtime given in hours
 
    user_weights = [0]*len(catnames); user_weights = map(float,user_weights)
    for i,j in enumerate(user_features):
        m = catnames.index(j)
        user_weights[m] = 1
        
    user_weights = np.asarray(user_weights); user_weights =  user_weights/sum(user_weights); 
    #user_weights = np.hstack((user_weights,0))
 
     
    ######################################################################
    ### filtering attractions from the complete list #####################
    ### dont want something with rating less than minimum allowed ########
    ### and which has none of the features selected by user ##############
    ### and no latitude longitude information ############################
    
    ###############################################################
    ## make an attraction_key dictionary of filtered attractions ##
    ## which maps attractions to indices also #####################
    ## also prepare other inputs to give to the optimal tour finder
    
 
    max_attractions = 20; 
    
    #if len(user_features) > 3: 
    #    max_attractions = 20; 
                 
    fin_attractions_mat = []; min_review_count = 20;
    for i,j in enumerate(attraction_names):
        if attraction_review_count[j] > min_review_count:
            j_features = categories_dict[j];
            fin_attractions_mat.append((j,att_prize(j_features,user_weights,attraction_review_count[j],attraction_ratings[j])))
            
    from operator import itemgetter
    fin_attractions_mat = sorted(fin_attractions_mat,key=itemgetter(1),reverse=True);
    fin_attractions_mat = fin_attractions_mat[0:max_attractions]
    
    fin_attractions = {};
    for i,j in enumerate(fin_attractions_mat):
        fin_attractions[j[0]] = i
    
 
                  
                          
    attraction_weights = np.zeros((len(fin_attractions),len(catnames)))            
    for i,j in enumerate(fin_attractions):
        attraction_weights[fin_attractions[j]][:] = categories_dict[j]
                        
    
    attraction_review_num = np.zeros((len(fin_attractions),1));
    fin_attraction_ratings = np.zeros((len(fin_attractions),1));
    fin_prize = np.zeros((len(fin_attractions),1));
    fin_prize_dict = {}
    for i,j in enumerate(fin_attractions):     
        attraction_review_num[fin_attractions[j]] = attraction_review_count[j]
        fin_attraction_ratings[fin_attractions[j]] = attraction_ratings[j] 
        fin_prize[fin_attractions[j]] = att_prize(categories_dict[j],user_weights,attraction_review_count[j],attraction_ratings[j])
        fin_prize_dict[j] = fin_prize[fin_attractions[j]]
    #################################################################
    ## getting the distance matrix between pairs of attractions #####
    ## distance is in miles #########################################
    ## then converting it to minutes with walking-rate 20 miles/hr ##
    #################################################################
    ## inserting recommended time for each attraction = 60 mins now #
    ## incorporating it in distance matrix (for the destination) ####
    ## the first point is also the home destination of user #########
    
    
    #n = len(fin_attractions.keys()); dist_fin = np.zeros((n+1,n+1))
    #for k1,k2 in enumerate(attraction_key):
    #    a = attraction_key[k2] # name of place one
    #    for m1,m2 in enumerate(attraction_key):
    #        b = attraction_key[m2] # name of place two
    #        if (a in fin_attractions.keys()) & (b in fin_attractions.keys()):
    #            i1 = fin_attractions[a]; i2 = fin_attractions[b];
    #            dist_fin[i1][i2] = attraction_distmat[k2][m2]
    #        
            
    # format of attraction key dictionaries
    # attraction_key 1:name
    # fin_attractions name:1   
    
    
    
  
    def get_distance_naive(p1,p2):
        # input example (44,117), latitude and longitude
        # returns distance in minutes driving at speed miles/hour
        drive_speed = 25; walk_speed = 4;
        R = 3961; c = 0.0174533 
        lat1 = p1[0]*c; lat2 = p2[0]*c; lon1 = p1[1]*c; lon2 = p2[1]*c;
        dlon = lon2 - lon1; dlat = lat2 - lat1 
        a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2 
        c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) ) ; d = R * c # in miles
        d1 = d*60/drive_speed + 10
        d2 = d*60/walk_speed
        return min(d1,d2)
    
    n = len(fin_attractions.keys());
    dist_fin = np.zeros((n+1,n+1))
    dist_fin_real = np.zeros((n+1,n+1))
    for i1,i2 in enumerate(attraction_key):
        a = attraction_key[i2]; 
        if a in fin_attractions.keys():
            y1 = fin_attractions[a];
        for j1,j2 in enumerate(attraction_key):
            b = attraction_key[j2];
            if b in fin_attractions.keys():
                y2 = fin_attractions[b];  
            if (a in fin_attractions.keys()) & (b in fin_attractions.keys()):
 
 
                orig_coord = attraction_latlon[attraction_key[i2]]
                dest_coord = attraction_latlon[attraction_key[j2]]

                driving_time = get_distance_naive(orig_coord,dest_coord)
                #if driving_time < 15:
                #    driving_time = 15;
                dist_fin[y1+1][y2+1] = driving_time + visit_times[attraction_key[j2]]
                dist_fin_real[y1+1][y2+1] = driving_time 
    for i1,j1 in enumerate(attraction_key):
        a = attraction_key[i1]; 
        if a in fin_attractions.keys():
            y1 = fin_attractions[a];
            orig_coord = home_latlon
            dest_coord = attraction_latlon[attraction_key[j1]]
            driving_time = get_distance_naive(orig_coord,dest_coord)
            dist_fin[y1+1][0] = driving_time 
            dist_fin_real[y1+1][0] = driving_time
            dist_fin[0][y1+1] = driving_time + visit_times[attraction_key[j1]]
            dist_fin_real[0][y1+1] = driving_time  
        
    
    
    ##################################################################
    ## making an input matrix for your optimal tour finder ###########
    ## including the user home in the input ########################## 
    
    
    attraction_weights = np.vstack(([1.0/len(catnames)]*(len(catnames)),attraction_weights))
    attraction_review_num = np.vstack(([10000],attraction_review_num))
    fin_attraction_ratings = np.vstack(([5],fin_attraction_ratings))                
    fin_prize = np.vstack(([5],fin_prize))    
 
 
    mytour, best_tour_len = optimal_tour_app(maxtime,dist_fin,attraction_weights,user_weights,attraction_review_num,fin_attraction_ratings,fin_prize)
    
    print mytour
    print 'and the real tsp time is', best_tour_len
    
    mytourfin = []; attraction_names = []; fin_latlons = []; latmat = [];
    toturl = 'https://www.google.com/maps/dir'
    attraction_desc = []; attraction_dur = []; attraction_start = [];
    for i,j in enumerate(mytour):
        if i > 0: 
            if i ==1 :
                attraction_start.append(dist_fin_real[mytour[i-1],mytour[i]])
  
            elif (i < len(mytour)) & (i!=1):
                attraction_start.append(attraction_start[-1] + dist_fin_real[mytour[i-1],mytour[i]]+xtime) 
        
                
        if j == 0:
            mytourfin.append('start from home')
            attraction_names.append('home')
            fin_latlons.append(home_latlon)
            latmat.append([home_latlon[0],home_latlon[1]])
            toturl = toturl+'/'+str(home_latlon)
        else:
            for attraction, num in fin_attractions.items():
                if num == j-1:
                    ab=attraction_title[attraction].replace(',','')
                    ab = ab.replace('&amp;','&')
                    mytourfin.append(ab)
                    attraction_names.append(attraction)
                    xtime = visit_times[attraction]
                    attraction_dur.append(int(xtime))
                    fin_latlons.append(attraction_latlon[attraction])
                    latmat.append([attraction_latlon[attraction][0],attraction_latlon[attraction][1]])
                    toturl = toturl+'/'+str(attraction_latlon[attraction])
                    xx = str(attraction_description[attraction]); xx=xx.replace('\'','')
                    xx=xx.replace('(',''); xx=xx.replace(')',''); xx=xx.replace(',','')
                    if len(xx) > 300:
                        xx = xx[0:300]; xx = xx + '...'
                    attraction_desc.append(xx) 
     
    print fin_latlons
    print attraction_start
    start_time = 9 
    import time
    for i,j in enumerate(attraction_start):
        j = (math.ceil(j/5.0))*5
        attraction_start[i] = time.strftime("%I:%M %p", time.gmtime(60*(start_time*60+j)))

        #attraction_start[i] = (attraction_start[i]%60)/100 + math.floor(attraction_start[i]/60) 
        #at_time = attraction_start[i];
        #attraction_start[i] = "%.2f" % attraction_start[i];
        #
        #if str(attraction_start[i]).split('.')[1] == 60:
        #    attraction_start[i]  = attraction_start[i]  + 1 - 0.60;
        #    attraction_start[i] = "%.2f" % attraction_start[i];
        #if (float(attraction_start[i])) > 12:
        #    attraction_start[i]  = str(attraction_start[i] -12) + ' pm' 
        #elif (float(attraction_start[i])) < 12:
        #    attraction_start[i]  = str(attraction_start[i]) + ' am' 
        #elif (math.floor(float((attraction_start[i])))) == 12:
        #    attraction_start[i]  = str(attraction_start[i]) + ' pm' 
    print attraction_start
    #import matplotlib.pyplot as plt
    #for i in range(len(fin_latlons)):
    #    if i < len(fin_latlons)-1:
    #        a = fin_latlons[i][0]; b = fin_latlons[i][1]
    #        c = fin_latlons[i+1][0]; d = fin_latlons[i+1][1]
    #    else:
    #        a = fin_latlons[i][0]; b = fin_latlons[i][1]
    #        c = fin_latlons[0][0]; d = fin_latlons[0][1]
    #    plt.plot([a,c],[b,d])
    #for i,j in enumerate(fin_attractions):
    #    print fin_prize_dict[j][0]
    #    a = fin_prize_dict[j][0]
    #    plt.scatter(attraction_latlon[j][0],attraction_latlon[j][1],s=a*100)
    #plt.show()    
    #
    
    
    
    return mytourfin,attraction_names,fin_latlons,toturl,attraction_desc,attraction_dur,attraction_start,latmat
         

#    my_attractions = ['History Museums','Museums,City Tours','Art Galleries','Historic Walking Areas','Walking Tours','Religious Sites',
#'Art Museums','Architectural Buildings','City Tours','Walking Tours','Nature and Parks',
#'Historic Sites','Boat Tours and Water Sports']  

#home_latlon = (37.8079996, -122.4177434);
#home_latlon = (37.77, -122.45);
#maxtime = 5; p = 5;
#address = 'Marriott Fisherman\'s Wharf San Francisco'
#home_latlon = get_latlon(address)
#user_features = ['theatre','tours','adventure and games','views']
#mytourfin,attraction_names,fin_latlons,toturl,attraction_desc,attraction_dur,attraction_start,latmat = main_fun_app(user_features,maxtime,home_latlon)

#print attraction_names 





