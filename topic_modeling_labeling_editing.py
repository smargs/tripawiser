
import pickle 
import nltk 
lemma = nltk.wordnet.WordNetLemmatizer()
from nltk.corpus import stopwords
mystopwords = set(stopwords.words('english'))
mystopwords.add('youre')
import numpy as np

import time
time1 = time.time()

min_reviews = 0; 

homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
with open(homeurl+'all_attractions.pickle') as f:
    attraction_names,attraction_urls  = pickle.load(f) 
    
attractions_num = len(attraction_names);
 
with open(homeurl+'all_attractions_info_new.pickle') as f:
    attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description,categories_key,categories_dict,catnames = pickle.load(f) 

with open(homeurl+'topicmodel_1.pickle') as f:
    reviews_key,reviews_vocab,review_dict,doc_topic,vocab,topic_word  = pickle.load(f) 
     
   
n_top_words = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))     

topic_list = {}; 
for i,j in enumerate(reviews_key):
    k = reviews_key[j];
    win_topic = list(doc_topic[k]).index(max(doc_topic[k]))
    
    str1 = homeurl + str(j+'_review');  
    num_lines_reviews = sum(1 for line in open(str1))
    
    if num_lines_reviews > min_reviews:
        if win_topic in topic_list.keys():
            topic_list[win_topic].append((attraction_title[j],max(doc_topic[k])))
        else:
            topic_list[win_topic] = []; topic_list[win_topic].append((attraction_title[j],max(doc_topic[k])))

import operator
topic_list_clean = [];
for i,j in enumerate(topic_list):
    try:
        mlist = [];
        xx = topic_list[i]
        topic_list[i] = sorted(xx,key=operator.itemgetter(1),reverse=True)
        for k,m in enumerate(topic_list[i]):
            mlist.append(m[0])
        topic_list_clean.append(mlist)
    except:
        print 'no topic #',i

topicmodel_topics = ['architecture','outdoor activities','shopping','culture','wellness', 
'','','beaches','tours','','theatre','tours','science','parks','','','tours','views',
'architecture','','museums','transport','','','adventure and games']        


mytopics = list(set(topicmodel_topics)); mytopics.pop(mytopics.index(''))
mytopics.pop(mytopics.index('transport')); mytopics.pop(mytopics.index('wellness'));

#topic_labels = {};
#topic_labels[0] = 'architecture' #
#topic_labels[1] = 'outdoor activities' #
#topic_labels[2] = 'shopping' # 
#topic_labels[3] = 'culture' # outlier 'Sea_Lion_Center' move to science
#topic_labels[4] = ''
#topic_labels[5] = '' #only Golden_Gate_Bridge move to independent
#topic_labels[6] = '' # wierd set AT_T_Park,Candlestick_Park to parks,The_View_Lounge to culture,Anchor_Brewing_Company to independent
#topic_labels[7] = 'beaches'
#topic_labels[8] = 'tours'
#topic_labels[9] = '' # only Cable car museum move to science
#topic_labels[10] = 'theatre' # 5 outliers Blazing_Saddles_Bike_Rentals_and_Tours,Basically_Free_Bike_Rentals,Bike_View_Bicycle_Rentals_and_Tours move to outdoor activities, Pier_23_Cafe,Lou_s_Fish_Shack move to independent
#topic_labels[11] = 'tours'
#topic_labels[12] = 'science'
#topic_labels[13] = 'parks' 
#topic_labels[14] = '' #weird set Alcatraz treat independent and also independent is Angel_Island_State_Park,Presidio_of_San_Francisco,Treasure_Island
#topic_labels[15] = '' # weird set 'Asian_Art_Museum','Musee_Mechanique', 'USS_Pampanito','SS_Jeremiah_O_Brien' independent
#topic_labels[16] = 'tours'
#topic_labels[17] = 'views'
#topic_labels[18] = 'architecture'
#topic_labels[19] = ''
#topic_labels[20] = 'museums'
#topic_labels[21] = 'transport'
#topic_labels[22] = '' #only Alcatraz_Cruises_LLC move to outdoor activities
#topic_labels[23] = '' #only San_Francisco_Bay move to beaches
#topic_labels[24] = 'adventure and games' # outlier The_Saloon move to culture
 


# modify the doc_top to add some outliers to their correct topics

doc_topic[reviews_key['Sea_Lion_Center']] = doc_topic[reviews_key['Aquarium_of_the_Bay']]
doc_topic[reviews_key['AT_T_Park']] = doc_topic[reviews_key['Golden_Gate_Park']]
doc_topic[reviews_key['Candlestick_Park']] = doc_topic[reviews_key['Golden_Gate_Park']]
doc_topic[reviews_key['The_View_Lounge']] = doc_topic[reviews_key['The_Castro']]
doc_topic[reviews_key['Cable_Car_Museum']] = doc_topic[reviews_key['The_Exploratorium']]

doc_topic[reviews_key['Blazing_Saddles_Bike_Rentals_and_Tours']] = doc_topic[reviews_key['Bay_City_Bike_Rentals_and_Tours']]
doc_topic[reviews_key['Basically_Free_Bike_Rentals']] = doc_topic[reviews_key['Bay_City_Bike_Rentals_and_Tours']]
doc_topic[reviews_key['Bike_View_Bicycle_Rentals_and_Tours']] = doc_topic[reviews_key['Bay_City_Bike_Rentals_and_Tours']]
doc_topic[reviews_key['Alcatraz_Cruises_LLC']] = doc_topic[reviews_key['Bay_Voyager']]
doc_topic[reviews_key['San_Francisco_Bay']] = doc_topic[reviews_key['Fort_Funston']]

independent = ['Golden_Gate_Bridge','Anchor_Brewing_Company','Pier_23_Cafe','Lou_s_Fish_Shack',
'Angel_Island_State_Park','Presidio_of_San_Francisco','Treasure_Island','Alcatraz',
'Asian_Art_Museum','Musee_Mecanique', 'USS_Pampanito','SS_Jeremiah_O_Brien','Asia_Society_and_Museum'
'Strawberry_Hill','Bliss_Dance_Esculture','1AM_Gallery','Mission_Bay_Conference_Center_at_UCSF','New_United_States_Mint','Royal_Thai_Spa',
'Kabuki_Springs_and_Spa','Defenestration_Building','Eurasian_Interiors_Chinese_Antiques_Furniture','Project_Zen_Massage_and_Bodywork','Mohandas_K_Gandhi_Gandhi_Statue']

# delete: Isla_Studio_Photography_Classes,Far_Fung_Places,Bay Area Rapid Transit,Scenic 49 Mile Drive
todelete = ['Isla_Studio_Photography_Classes,Far_Fung_Places,Bay Area Rapid Transit,Scenic 49 Mile Drive']

# normalize distribution of each attraction in doc_topic 
new_doc_topic = {};
for i, j in enumerate(reviews_key):
    if j not in independent:
        vec = doc_topic[reviews_key[j]]; vec1 = [0]*len(mytopics)
        for k,m in enumerate(vec):
            if topicmodel_topics[k] in mytopics:
                x = mytopics.index(topicmodel_topics[k])
                vec1[x] = vec1[x] + m
        new_doc_topic[j] = vec1/sum(vec1)
            


# add topics food, histrory, art and obtain distributions for attractions 
# by doing frequency count of words in mytopics
# especially update attractions not in reviews_key or in independent 

# update other attractions (which are in reviews_key and 
# not independent) as well

mytopics.append('food and drink'); mytopics.append('art')
mytopics.append('history'); mytopics.append('wellness')
sub = {}; sub['food and drink'] = ['food','wine','eat']; 
sub['outdoor activities'] = ['outdoor','activities'];
sub['adventure and games'] = ['adventure','games'];
sub['wellness'] = ['spa','massage']
const = 0.1
for k,m in enumerate(attraction_names):
    if m in reviews_key.keys():
        x = np.zeros((1,len(mytopics))); x = x.astype(float); x = x[0]
        for i,j in enumerate(mytopics):
            if j in sub.keys():
                wli = sub[j]
            else:
                wli = [j]
            for n,p in enumerate(wli):
                x[i] =  review_dict[reviews_key[m],[reviews_vocab[p]]]
        if sum(x) > 0:
             x = x/sum(x)
        if m in independent:
            new_doc_topic[m] = x
        else:
            new_doc_topic[m] = np.hstack((new_doc_topic[m],const*x[-4:]))
            new_doc_topic[m] = new_doc_topic[m]/sum(new_doc_topic[m])
    else:
        new_doc_topic[m] = [0]*len(mytopics)
    if m in todelete:
        new_doc_topic[m] = [0]*len(mytopics)
        
a = [];             
for k,m in enumerate(attraction_names):
    a.append(len(new_doc_topic[m]))                
    
with open(homeurl+'attraction_categories.pickle', 'w') as f:
    pickle.dump([mytopics,new_doc_topic], f)
 

#########################################################################
### cosine similarity ###################################################
#########################################################################
 
 
# compare = ['history','parks']; 
compare = ['history','parks']; compare_ind = [];
for i,j in enumerate(compare):
    compare_ind.append(mytopics.index(j))

tot_winner = {}       

for i,j in enumerate(attraction_names):
     winner = list(new_doc_topic[j]).index(max(new_doc_topic[j]))
     win = max(new_doc_topic[j])
     if (winner in compare_ind) & (win>0):
         if winner not in tot_winner.keys():
             tot_winner[winner] = [];  
         tot_winner[winner].append((j,win))     

from operator import itemgetter   
tot = 0;         
for i, j in enumerate(tot_winner): 
    tot_winner[j] = sorted(tot_winner[j],key=itemgetter(1),reverse=True)
    tot = tot + len(tot_winner[j])
        
mydoc = np.zeros((10,len(review_dict[0])))
c = 0;
for i, j in enumerate(tot_winner):
    d = 0;
    for k,m in enumerate(tot_winner[j]):
        if d < 5:
            mydoc[c] = review_dict[reviews_key[m[0]]]
            c = c + 1
            d = d + 1

import math
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)


mat = np.zeros((10,10))
for i in range(10):
    for j in range(10):
        mat[i][j] = cosine_similarity(mydoc[i],mydoc[j])

import matplotlib.pyplot as plt
plt.imshow(mat, interpolation='none', cmap=plt.cm.Blues)        
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 