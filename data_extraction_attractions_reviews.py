import requests
from bs4 import BeautifulSoup
import unicodedata
import string
import pickle


####################################################################
## this file scrapes reviews of all attractions in san francisco ###
####################################################################

## getting list of attractions ##
#################################
baseurl = 'http://www.tripadvisor.com/'
homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
 
with open(homeurl+'all_attractions.pickle') as f:
    attraction_names,attraction_urls  = pickle.load(f) 
 
with open(homeurl+'all_attractions_info_new.pickle') as f:
    attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count = pickle.load(f) 
 

print 'attractions collected'

## decide how much to scrape ###
################################
attractions_num = len(attraction_urls); 
review_pages_to_scrap = 3000; 
 
## initialize ##################
################################
seps = ["ago","yesterday","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]
exclude = set(string.punctuation); exclude.remove('.'); exclude.remove(',')

 

reviews_scraped = {}; review_highlights_scraped = {}; 

    
## start scraping ##############
################################

print 'scraping started'

for k in range(0,attractions_num,1):
    
    count = 0; counth = 0; atype = []; itype = [];
    turl = str(baseurl)+str(attraction_urls[k])
 
    ## creating a list of urls of all reviews for an attraction ##
    ##############################################################
    aurl = [];
    a1 = turl.split("Reviews");  review_pages = attraction_review_count[attraction_names[k]]/10+1;
    review_pages_to_scrap_now = min(review_pages_to_scrap,review_pages)
    for f in range(review_pages_to_scrap_now):
        a2 = str(a1[0])+"Reviews-or"+str(f+1)+"0" + str(a1[1])
        aurl.append(a2);
    
    ## getting reviews ##
    #####################
    str1 = homeurl + str(attraction_names[k]+'_review'); text1_file = open(str1, "w")
    str2 = homeurl + str(attraction_names[k]+'_highlight'); text2_file = open(str2, "w")
    
    for f in range(len(aurl)):
        
        # scrape a single page of reviews
        if f/100 == float(f)/100:
            print "attraction #", k, 'review page #',f
        try:
            turl = aurl[f]
            contents = requests.get(turl)
            soup = BeautifulSoup(contents.text, "html.parser")
            q = soup.find_all('p',class_='partial_entry')
            r = soup.find_all('span',class_='noQuotes')
            
        except:
            break
             
        ## scrape a review ###
        ######################
        for p in range(len(q)):
            pp=str(q[p]).split("partial_entry"); pp = pp[1]; 
            
            pp=unicode(pp, "utf-8")
            pp = unicodedata.normalize('NFKD', pp).encode('ascii','ignore')
 
            pp=pp.split("\n"); pp = pp[1];  
 
            #pp = pp.replace(".", "")
            pp = ''.join(ch for ch in pp if ch not in exclude)
             
            pp = pp+'\n'+'\n'
            if 'span' not in pp:
                text1_file.write(pp)            
                count = count + 1;
            
        ## scrape a review heading ##
        #############################
        for p in range(len(r)):
            d = str(r[p])[23::]; d = d[:-7]; 
            d = unicode(d, "utf-8")
            d = unicodedata.normalize('NFKD', d).encode('ascii','ignore')
            
            #d = d.replace(".", "")
            d = ''.join(ch for ch in d if ch not in exclude)
            if len(d) > 0:
                if (d[0] == 'p') & (d[-1]=='p'):
                    d=[]
                else:
                    d = d+'\n'+'\n'
                    text2_file.write(d) 
                    counth = counth + 1
    
    reviews_scraped[attraction_names[k]] = count; 
    review_highlights_scraped[attraction_names[k]] = counth; 
    attraction_type[attraction_names[k]] = atype
    attraction_info[attraction_names[k]] = itype 
    
    text1_file.close()
    text2_file.close()
    
    print 'attraction' ,k, 'scraped'
   
    with open(homeurl+'all_attractions_scraping_details.pickle', 'w') as g:
        pickle.dump([reviews_scraped, review_highlights_scraped], g)
    




     







