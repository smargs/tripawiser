##################################################
### tour builder #################################

def main_fun(user_features,maxtime,home_latlon):

    import math
    import pickle
    import numpy as np
    from optimal_tour import optimal_tour
    from optimal_tour import rating_score
    
    ##################################################
    ### loading all data #############################
    
    homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
    #homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
    with open(homeurl+'all_attractions.pickle') as f:
        attraction_names,attraction_urls  = pickle.load(f) 
         
 
    with open(homeurl+'all_attractions_info_new.pickle') as f:
        attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description,categories_key,categories_dict,catnames = pickle.load(f) 
        
    with open(homeurl+'attraction_categories.pickle') as f:
        catnames,categories_dict = pickle.load(f) 
    print catnames
    
  
    ###################################################
    ## including the visit times ######################
    ## setting all to 60 minutes right now ############
    ## will have to be extracted eventually ###########
    visit_times = {}
    for i,j in enumerate(attraction_names):
        visit_times[j] = 20;
        
            
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
    
    match_threshold = 0.1; ep = 0.001; max_attractions = 25; min_review_count = 20;
    flag = 0
    while flag == 0:
        fin_attractions = {}; count = 0; flag = 0;
        for i,j in enumerate(attraction_names): 
            if attraction_review_count[j] > min_review_count:
                if j in attraction_latlon.keys():  
                    j_features = categories_dict[j];
                    if np.dot(j_features,user_weights) > match_threshold:
                        np.dot(j_features,user_weights)*np.log(attraction_review_count[j])*rating_score(attraction_ratings[j])  
                        fin_attractions[j] = count;  
                        count = count + 1
        if count > 0:
            last_nonzero_set = fin_attractions
        if count > max_attractions:
            match_threshold = match_threshold + ep
        else:
            flag = 1
            break
        
    if len(fin_attractions) == 0:
        fin_attractions = last_nonzero_set
    print len(fin_attractions), 'were shortlisted'
    
    
    if len(fin_attractions) > max_attractions:
        new_fin = {};
        for i,j in enumerate(fin_attractions):
            if fin_attractions[j] < max_attractions:
                new_fin[j] = fin_attractions[j]
        fin_attractions = new_fin
        print 'and they had to be brought down to' ,len(fin_attractions),' attractions'       
        
     
     
                          
    attraction_weights = np.zeros((len(fin_attractions),len(catnames)))            
    for i,j in enumerate(fin_attractions):
        attraction_weights[fin_attractions[j]][:] = categories_dict[j]
                        
    
    attraction_review_num = np.zeros((len(fin_attractions),1));
    fin_attraction_ratings = np.zeros((len(fin_attractions),1));
    for i,j in enumerate(fin_attractions):     
        attraction_review_num[fin_attractions[j]] = attraction_review_count[j]
        fin_attraction_ratings[fin_attractions[j]] = attraction_ratings[j] 
        
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
        # returns distance in minutes driving at 30 miles/hour
        R = 3961; c = 0.0174533 
        lat1 = p1[0]*c; lat2 = p2[0]*c; lon1 = p1[1]*c; lon2 = p2[1]*c;
        dlon = lon2 - lon1; dlat = lat2 - lat1 
        a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2 
        c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) ) ; d = R * c 
        return d*60/30
    
    n = len(fin_attractions.keys());
    dist_fin = np.zeros((n+1,n+1))
  
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
                 
                dist_fin[y1+1][y2+1] = driving_time + attraction_time[attraction_key[j2]]
    
    for i1,j1 in enumerate(attraction_key):
        a = attraction_key[i1]; 
        if a in fin_attractions.keys():
            y1 = fin_attractions[a];
            orig_coord = home_latlon
            dest_coord = attraction_latlon[attraction_key[j1]]
            driving_time = get_distance_naive(orig_coord,dest_coord)
            dist_fin[y1+1][0] = driving_time
            dist_fin[0][y1+1] = driving_time + attraction_time[attraction_key[j1]]
 
        
    
    
    ##################################################################
    ## making an input matrix for your optimal tour finder ###########
    ## including the user home in the input ########################## 
    
    
    attraction_weights = np.vstack(([1.0/len(catnames)]*(len(catnames)),attraction_weights))
    attraction_review_num = np.vstack(([10000],attraction_review_num))
    fin_attraction_ratings = np.vstack(([5],fin_attraction_ratings))                
 
    mytour = optimal_tour(maxtime,dist_fin,attraction_weights,user_weights,attraction_review_num,fin_attraction_ratings)
    print mytour
    
    mytourfin = []; attraction_names = []; fin_latlons = [];
    toturl = 'https://www.google.com/maps/dir'
    attraction_desc = [];
    for i,j in enumerate(mytour):
        if j == 0:
            mytourfin.append('start from home')
            attraction_names.append('home')
            fin_latlons.append(home_latlon)
            toturl = toturl+'/'+str(home_latlon)
        else:
            for attraction, num in fin_attractions.items():
                if num == j-1:
                    mytourfin.append(attraction_title[attraction])
                    attraction_names.append(attraction)
                    fin_latlons.append(attraction_latlon[attraction])
                    toturl = toturl+'/'+str(attraction_latlon[attraction])
                    xx = str(attraction_description[attraction]); xx=xx.replace('\'','')
                    xx=xx.replace('(',''); xx=xx.replace(')',''); xx=xx.replace(',','')
                    attraction_desc.append(xx) 
    print fin_latlons
  
    
    return mytourfin,attraction_names,fin_latlons,toturl,attraction_desc
 

home_latlon = (37.707486, -122.420460); maxtime = 3.5; p = 5;
user_features = ['history','science']
mytourfin,attraction_names,fin_latlons,toturl,attraction_desc = main_fun(user_features,maxtime,home_latlon)

 

import json
import urllib2
import urllib

def get_latlon(address): 
    encodedAddress = urllib.quote_plus(address)
    data = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=" + encodedAddress + '&sensor=false').read()
    location = json.loads(data)['results'][0]['geometry']['location']
    lat = location['lat']
    lon = location['lng']
    return lat, lon 
