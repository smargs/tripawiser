import pandas as pd
from bs4 import BeautifulSoup
import requests
import pickle

def data_extraction_attractions_list():

    url_list = ['http://www.tripadvisor.com/Attractions-g60713-Activities-San_Francisco_California.html',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa30-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa60-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa90-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa120-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa150-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa180-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa210-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa2400-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa270-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa300-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa330-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa360-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa390-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa420-San_Francisco_California.html#ATTRACTION_LIST',
    'http://www.tripadvisor.com/Attractions-g60713-Activities-oa450-San_Francisco_California.html#ATTRACTION_LIST',]
    
    attraction_urls = []; attraction_names = [];
    
    while url_list:
        contents = requests.get(url_list[0])
        url_list.pop(0)
        soup = BeautifulSoup(contents.text, "html.parser")
        a = soup.get_text()
        for link in soup.find_all('a'):  
            b=link.get('href')
            if type(b) is unicode:
                if '/Attraction_Review-g60713' in b: 
                    d = b.split("Reviews-"); d = d[1]; d = d.split("San_Francisco_California.html"); 
                    d = d[0]; d = str(d); d = d[:-1]
                    if d not in ['Pacific_Palisades_Farmer_s_Market','San_Francisco_Bay_Bridge','Gold_Country','Forneris_Farms']:
                    # these places are not in SF and the Bay Bridge is not very important  
                        if (d not in attraction_names) & ('htm' not in d):
                            attraction_names.append(d);
                            attraction_urls.append(b);
        
    
    homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
    with open(homeurl+'all_attractions.pickle', 'w') as f:
        pickle.dump([attraction_names,attraction_urls], f)
     
        
    return attraction_names,attraction_urls


    


attraction_names,attraction_urls = data_extraction_attractions_list() 
     
 