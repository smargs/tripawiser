####################################################################
## this file computes a topic model for all attraction reviews #####
####################################################################


import pickle
from nltk.corpus import words
import nltk 
lemma = nltk.wordnet.WordNetLemmatizer()
from nltk.corpus import stopwords
mystopwords = set(stopwords.words('english'))
mystopwords.add('youre')
import numpy as np

import time
time1 = time.time()

min_reviews = 50; 

homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
with open(homeurl+'all_attractions.pickle') as f:
    attraction_names,attraction_urls,  = pickle.load(f) 

attractions_num = len(attraction_names);

homeurl = '/Users/Pushkarini/Dropbox/Push/insight_project/ta_reviews/'
with open(homeurl+'all_attractions_info_new.pickle') as f:
    attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description,categories_key,categories_dict,catnames = pickle.load(f) 
    

## word cleaners ###############
################################
allwords = set(words.words())
words_in_titles = set((' '.join(attraction_title.values())).split(' '))
allwords = set(list(allwords)+list(words_in_titles))
 
       
def is_word(myword):
    flag = 0;
    if any(char.isdigit() for char in myword) == False:
        if myword in allwords:
            flag = 1;
    if flag == 1:
        return True
    else:
        return False
    
def is_not_number(myword):
    flag = 0;
    if any(char.isdigit() for char in myword) == False:
        flag = 1;
    if flag == 1:
        return True
    else:
        return False


## making a dictionary of all words excluding stopwords
reviews_vocab = {};  highlights_vocab = {}; count1 = 0; count2 = 0;
for k in range(attractions_num):
    try:
        str1 = homeurl + str(attraction_names[k]+'_review');  
        str2 = homeurl + str(attraction_names[k]+'_highlight');  
 
        with open(str1, "r") as ins:
            for line in ins:
                line = line.replace("\n"," "); line = line.replace(","," "); line = line.replace("."," ")
                cline = line
                cline = [word for word in cline.split() if word not in mystopwords]
                for i,j in enumerate(cline):
                    j = j.lower()
                     
                    if (j not in reviews_vocab):
                        if is_not_number(j):        
                            reviews_vocab[j] = count1; count1 = count1 + 1;
                        if j == 'headphonesits':
                            print str1
                            
        with open(str2, "r") as ins:
            for line in ins:
                line = line.replace("\n"," "); line = line.replace(","," "); line = line.replace("."," ")
                cline = line
                cline = [word for word in cline.split() if word not in mystopwords]
                for i,j in enumerate(cline):
                    j = j.lower()
                     
                    if j not in highlights_vocab:
                        if is_not_number(j):     
                            highlights_vocab[j] = count2; count2 = count2 + 1;
    except: 
        print 'vocabulary from',str(attraction_names[k]), 'not extracted'                    

print 'total words in reviews are', len(reviews_vocab)
print 'total words in highlights are', len(highlights_vocab)


review_dict = np.zeros((attractions_num,len(reviews_vocab))) 
highlight_dict = np.zeros((attractions_num,len(highlights_vocab))) 

 

k1 = 0; k2 = 0;
reviews_key = {}; highlights_key = {}
for k in range(attractions_num):
     
        
    str1 = homeurl + str(attraction_names[k]+'_review');  
    str2 = homeurl + str(attraction_names[k]+'_highlight'); 
    try:
        num_lines_reviews = sum(1 for line in open(str1))
        num_lines_highlights = sum(1 for line in open(str2))
        
        if num_lines_reviews > 0: 
            with open(str1, "r") as ins:
                for line in ins:
                    line = line.replace("\n"," "); line = line.replace(","," "); line = line.replace("."," ")
                    cline = line
                    cline = [word for word in cline.split() if word not in mystopwords]
                    for i,j in enumerate(cline):
                        j = j.lower()
                        if is_not_number(j): 
                            x = reviews_vocab[j];
                            review_dict[k1][x] = review_dict[k1][x] + 1
            reviews_key[attraction_names[k]] = k1; k1 = k1 + 1;
            
        if num_lines_highlights > 0:                   
            with open(str2, "r") as ins:
                for line in ins:
                    line = line.replace("\n"," "); line = line.replace(","," "); line = line.replace("."," ")
                    cline = line
                    cline = [word for word in cline.split() if word not in mystopwords]
                    for i,j in enumerate(cline):
                        j = j.lower()
                        if is_not_number(j): 
                            x = highlights_vocab[j];
                            highlight_dict[k2][x] = highlight_dict[k2][x] + 1
            highlights_key[attraction_names[k]] = k2; k2 = k2 + 1;
    except: 
        print 'reviews for',str(attraction_names[k]), 'not extracted'  

    
review_dict = review_dict[0:k1,:];        
                
with open(homeurl+'review_bow.pickle', 'w') as f:
    pickle.dump([reviews_key,reviews_vocab,review_dict,highlights_vocab,highlight_dict], f)
      
    
####################################################################
####################################################################    
## adding categories to bag of words ###############################           

X = review_dict

pc = 5;

if pc > 0:
    # edit X to have put category names in bag of words as well ##
    # first calculate how many words to add ######################
    count1 = len(reviews_vocab); count_base = count1;
    for i,j in enumerate(reviews_key):
        types = attraction_type[j]; 
        for m,k in enumerate(types):
            k = k.replace(' ','')
            if k not in reviews_vocab:
                reviews_vocab[k] = count1; count1 = count1 + 1
    
    X = np.hstack((X,np.zeros((len(reviews_key),count1-count_base))))
    for i,j in enumerate(reviews_key):
        types = attraction_type[j]; 
        for m,k in enumerate(types):
            k = k.replace(' ','')
            f = reviews_key[j];
            totwords_in_review = sum(X[f,:]);
            totwords_to_add = int(float(totwords_in_review)*pc/100);
            X[f,reviews_vocab[k]] = totwords_to_add
        
        
             
##########################################################################
##########################################################################    
## python LDA ############################################################

topnum = 25; 
import lda 
X = X.astype(int); 
model = lda.LDA(n_topics=topnum, n_iter=100, random_state=1); model.fit(X)  
topic_word = model.topic_word_ ; 
vocab = tuple(reviews_vocab);

doc_topic = model.doc_topic_


with open(homeurl+'topicmodel_1.pickle', 'w') as f:
    pickle.dump([reviews_key,reviews_vocab,review_dict,doc_topic,vocab,topic_word], f)
 

        
        

    
###########################################################################
###########################################################################       
## gensim hdp #############################################################


#from gensim.models.hdpmodel import HdpModel as hdpmodel  
# 
#id2word = {};
#for i,j in enumerate(vocab):
#    id2word[i] = j
#
#corpus1 = [];
#for i,j in enumerate(X):
#    x = j; y = [];
#    for k,m in enumerate(x):
#        if m > 0:
#            y.append((k,m)) 
#    corpus1.append(y)
#    
#hdp = hdpmodel(corpus1, id2word)     
#hdp.print_topics(topics=5, topn=10) 
#   
#print 'current vocab is of length', len(vocab)
#print 'previous vocab was of length 47912'

    
    
    
    
    
    
    
    
    