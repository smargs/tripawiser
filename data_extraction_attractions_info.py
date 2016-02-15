import requests
from bs4 import BeautifulSoup
import string
import pickle
import json, urllib, urllib2

## getting list of attractions ##
#################################
baseurl = 'http://www.tripadvisor.com/'
homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
 
with open(homeurl+'all_attractions.pickle') as f:
    attraction_names,attraction_urls,  = pickle.load(f) 
  
print 'attractions collected'

## decide how much to scrape ###
################################
attractions_num = len(attraction_urls); 
 
## initialize ##################
################################
seps = ["ago","yesterday","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]
exclude = set(string.punctuation); 
attraction_type = {}; attraction_info = {}; attraction_address = {};
attraction_opentime = {}; attraction_closetime = {}; 
attraction_ratings = {}; attraction_review_count = {};
attraction_title = {}; attraction_description = {};

reviews_scraped = {}; review_highlights_scraped = {}; 

    
## start scraping ##############
################################

print 'scraping started'

for k in range(attractions_num):
      
    count = 0; counth = 0; atype = []; itype = [];

    ## getting attraction names review count and other info ##
    #######################################
    # get some attraction details from first review page
    turl = str(baseurl)+str(attraction_urls[k])
    contents = requests.get(turl)
    soup = BeautifulSoup(contents.text, "html.parser")
    
    a1 = str(soup).split('<h1'); a11 = a1[1].split('</h1>')
    a13 = a11[0].split(">")[1]
    attraction_title[attraction_names[k]] = a13

    
    
    a12 = soup.find_all('div',class_='rs rating')
    
    try:
        attraction_ratings[attraction_names[k]] = (str(a12).split("img alt")[1]).split("of")[0][2::] 
    except:
        attraction_ratings[attraction_names[k]] = 0;
        print 'rating for' ,attraction_names[k], 'not recorded' 
    
    
    
    try:
        a12 = str(a12).split("reviewCount")[1]
        a12 = a12.split('>')[1]; a12 = a12.split('</')[0]; 
        a12 = a12.replace(",", ""); a12 = a12.replace('Reviews',''); 
        a12 = a12.replace('Review',''); review_num = int(a12)
    except:
        print 'review count for' ,attraction_names[k], 'not recorded'
        review_num = 0
    attraction_review_count[attraction_names[k]] = review_num
    
    
    
    
    try:
        a13 = soup.find_all('div',class_='times'); 
        if len(a13) > 0:
            a13 = str(a13)[40::]; a13 = a13[:-15];
            op = a13.split('-')[0]; cl = a13.split('-')[1]; 
            opt = op[:-4]; clt = cl[1::]; clt = clt[:-3];
            opt = opt.replace(':',""); clt = clt.replace(':',"")
    
            if 'am' in op:
                attraction_opentime[attraction_names[k]] = int(opt)
            else:
                attraction_opentime[attraction_names[k]] = 1200 + int(opt)
                
            if cl[-3] == 'a':
                attraction_closetime[attraction_names[k]] = int(clt)
            else:
                attraction_closetime[attraction_names[k]] = 1200 + int(clt)
    except:
        print 'time for attraction' ,attraction_names[k], 'not recorded'
        attraction_opentime[attraction_names[k]] = 1000;
        attraction_closetime[attraction_names[k]] = 1600;
        
                    
    this_add = "";
    a12 = soup.find_all('span',class_='street-address');
    if a12:     
        street = (str(a12).split('>')[1]).split('<')[0];
    a12 = soup.find_all('span',class_='locality');
    if a12:
        city = (str(a12).split('>')[2]).split('<')[0];
        state = (str(a12).split('>')[4]).split('<')[0];
        zipcode = (str(a12).split('>')[6]).split('<')[0];
    this_add = street + " " + city + " " + state + " " +zipcode
    this_add = this_add.replace("&amp;", "and"); 
    this_add = this_add.replace("]", "");
    
    attraction_address[attraction_names[k]] = this_add
 
    s = soup.find_all('div',class_='detail')
    
    for p in range(len(s)):
        y=s[p]; y = str(y).replace('"',""); 
        if "<div class=detail>" in y:
            s1 = y.split(".html>"); 
            if len(s1) == 1:
                try:
                    s2 = s1[0].split("<b>")[1]
                    s3 = s2.split("</b>")[0]
                    s4 = s2.split("</b>")[1]
                    s4 = s4.split("</div>"); s4 = s4[0];
                    itype.append(s3+s4);
                except:
                    print 'one information piece lost for attraction ', str(attraction_names[k])
            else:
                s1 = y.split("</a>")
                for m in range(len(s1)):
                    ss = s1[m].split("html>")
                    if len(ss)>1:
                        sd = ss[1]; sd = sd.replace("&amp;", "and")
                        atype.append(sd); 
                            
    
    attraction_type[attraction_names[k]] = atype
    attraction_info[attraction_names[k]] = itype 
    
    
    try:
        s = soup.find_all('div',class_='listing_details')
        s = (str(s).split('<p>')[1]).split('</p>')[0]
        attraction_description[attraction_names[k]] = s;
    except:
        attraction_description[attraction_names[k]] = 'This attraction is listed in the', ', '.join(attraction_type[attraction_names[k]]), 'categories in San Francisco'
        print 'description for', str(attraction_names[k]), 'not scraped'
    
  
    print 'attraction' ,k, ' info scraped'
    
## reverse of attraction type ##
################################
attraction_typer = {}

for i,j in enumerate(attraction_type): 
    name = j; types = attraction_type[j];
    for i1,j1 in enumerate(types):
        if j1 not in attraction_typer.keys():
            attraction_typer[j1] = set(); attraction_typer[j1].add(name)
        else:
            attraction_typer[j1].add(name)
  
        
##############################################################
### cleaning dictionaries getting them to right format etc ### 

for i,j in enumerate(attraction_ratings):
    aa = attraction_ratings[j]; 
    if aa != 0:
        aa = float(aa[:-1])
    attraction_ratings[j] = aa;


for i,j in enumerate(attraction_names):
        a1 = attraction_title[j]
        a1 = a1.replace(', San Francisco','')
        attraction_title[j] = a1;            
                    
### getting recommended visit times #################
#####################################################

attraction_time = {};
for i,j in enumerate(attraction_info):
    x = attraction_info[j]; flag = 0;
    for k,m in enumerate(x):
        if 'Recommended' in m:  
            if '&lt;1 hour' in m:
                attraction_time[j] = 45; flag = 1;
            elif 'More than' in m:
                m = m.replace('More than 3 hours','')
                attraction_time[j] = 210; flag = 1;
            else:
                m = m.replace('Recommended length of visit:','')   
                m = m.replace('hours',''); m=m.replace(' ','')
                attraction_time[j] = (int(m[0])*0.25 + int(m[2])*0.75)*60
                flag = 1;
    if flag == 0: # no recommended time found!
        attraction_time[j] = 30; 
           
                                    
         
### address getter and distance matrix calculator ###
#####################################################
def get_latlon(address): 
    encodedAddress = urllib.quote_plus(address)
    data = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=" + encodedAddress + '&sensor=false').read()
    location = json.loads(data)['results'][0]['geometry']['location']
    lat = location['lat']
    lon = location['lng']
    return lat, lon 

attraction_key = {}; count = 0;
for i,j in enumerate(attraction_names): 
    if attraction_address[j] == ' San Francisco CA ':
        attraction_address[j] = attraction_title[j] + ' San Francisco CA'
    attraction_key[i] = j
         
with open(homeurl+'bad_addresses.pickle') as f:
    bad_addresses  = pickle.load(f)         
 
attraction_latlon = {};  
for k in range(10):
    for i,j in enumerate(attraction_names):
        if j in bad_addresses:
            attraction_address[j] = attraction_title[j] + ' San Francisco CA'        
        else:
            this_address = attraction_address[j]; 
        if j not in attraction_latlon.keys():
            try: 
                lat, lon = get_latlon(this_address)
                if (lat > 37) & (lon <121):
                    attraction_latlon[j] = (lat,lon) 
            except:
                x = 0

if len(attraction_latlon) != len(attraction_key):
    print 'all addresses not collected !!'
    

import json as simplejson
import numpy as np
def get_distance(orig_coord,dest_coord):
    # this returns driving time in seconds !!!!
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
    result= simplejson.load(urllib.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration']['value']       
    return driving_time

import math
def get_distance_naive(p1,p2):
    # input example (44,117), latitude and longitude
    # returns distance in minutes driving at 30 miles/hour
    R = 3961; c = 0.0174533 
    lat1 = p1[0]*c; lat2 = p2[0]*c; lon1 = p1[1]*c; lon2 = p2[1]*c;
    dlon = lon2 - lon1; dlat = lat2 - lat1 
    a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2 
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) ) ; d = R * c 
    return d*60/30

attraction_distmat = np.zeros((len(attraction_key),len(attraction_key)));
done = np.zeros((len(attraction_key),len(attraction_key)));
for i1,i2 in enumerate(attraction_key):
    for j1,j2 in enumerate(attraction_key):
        if i2 == j2:
            done[i2][j2] = 1
        if done[i2][j2] == 0:
            orig_coord = attraction_latlon[attraction_key[i2]]
            dest_coord = attraction_latlon[attraction_key[j2]]
            try:
                driving_time = get_distance_naive(orig_coord,dest_coord)
                attraction_distmat[i2][j2] = driving_time + attraction_time[attraction_key[j2]]
                done[i2][j2] = 1
            except:
                x = 0;
 
with open(homeurl+'all_attractions_info.pickle', 'w') as f:
    pickle.dump([attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description], f)
      
    
    
    
     
     