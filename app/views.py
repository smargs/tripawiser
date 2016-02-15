from flask import render_template, request
from app import app 
import pickle


#import sys
#sys.path.insert(0, '/home/smargs/Dropbox/Push/insight_project/')

from main_fun_app import main_fun_app
from main_fun_app import get_latlon

#import requests
#start = requests.args.get('start')

#homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
#homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
homeurl = '/home/smargs/app/data/'
#homeurl = 'app/static/data/'

with open(homeurl+'all_attractions_info_new.pickle') as f:
    attraction_info,attraction_title,attraction_time,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_key,attraction_distmat,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count,attraction_description,categories_key,categories_dict,catnames = pickle.load(f) 
with open(homeurl+'attractions_categories_new.pickle') as f:
    catnames,categories_dict = pickle.load(f)            

with open(homeurl+'all_attractions_new.pickle') as f:
    attraction_names,attraction_urls  = pickle.load(f) 

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
        title = 'Home',
        )

@app.route('/db')
def cities_page():
	db= mdb.connect(user="root", host="localhost", db="world", charset='utf8')
	with db: 
		cur = db.cursor()
		cur.execute("SELECT Name FROM City LIMIT 15;")
		query_results = cur.fetchall()
	cities = ""
	for result in query_results:
		cities += result[0]
		cities += "<br>"
	return cities

@app.route("/db_fancy")
def cities_page_fancy():
	db= mdb.connect(user="root", host="localhost", db="world", charset='utf8')
	with db:
		cur = db.cursor()
		cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

		query_results = cur.fetchall()
	cities = []
	for result in query_results:
		cities.append(dict(name=result[0], country=result[1], population=result[2]))
	return render_template('cities.html', cities=cities) 

@app.route('/index')
def cities_input():
  return render_template("index.html")
 

@app.route('/output')
def cities_output():
  #pull 'ID' from input field and store it
  #interest = request.args.get('ID')
  #interest = request.args.get('ID')
  #all_interests = interest.split(',') 
  #the_result1 = []; user_features = [];
  #for i,j in enumerate(all_interests):          
  #    the_result1.extend(attraction_typer[j])
  #    user_features.append(str(j))
 
  
  #
  #interest1 = request.args.get('int_1')
  #interest2 = request.args.get('int_2')   
  #user_features = [];
  #if interest1 == 'on':
  #    user_features.append('History Museums')
  #if interest2 == 'on':
  #    user_features.append('Historic Sites')
  
  #p = request.args.get('pnum'); p = float(p)
  
 try:
    address = request.args.get('ID')
    home_latlon = get_latlon(address)
 except: 
    home_latlon = (37.8079996, -122.4177434);
 homeflag = 1;
 if (home_latlon[0] > 37.7) & (home_latlon[0] < 37.81):
     if (home_latlon[1] < -122.37) & (home_latlon[1] > -122.51):
         homeflag = 0;
 if homeflag == 1:
     home_latlon = (37.8079996, -122.4177434);
 
 user_features = [];
 button_num = len(catnames); interest_list = catnames;#['History Museums','Historic Sites','Historic Walking Areas'];
 for i in range(button_num):
      but = 'int_' + str(i+1);
      print but
      if request.args.get(but) == 'on':
          user_features.append(interest_list[i]);
  
 if len(user_features) == 0:
      user_features.append('history'); user_features.append('architecture')
      

 if len(user_features)==16:
     user_features.pop(user_features.index('wellness'));
      
 
 try:
    maxtime = request.args.get('ID1'); maxtime = float(maxtime)
 except:
    maxtime = 3;   
 if maxtime > 9:
     maxtime = 9;
 if maxtime < 2:
     maxtime = 2;
     
 import numpy as np 
 print 'maxtime is ', maxtime
 the_result,attraction_list_names,fin_latlons,toturl,attraction_desc,attraction_dur,attraction_start,latmat = main_fun_app(user_features,maxtime,home_latlon);  
 print len(fin_latlons)
 mapcenter = sum(np.asarray(fin_latlons),0)/len(fin_latlons); mapcenter = str(list(mapcenter));
 mapcenter = mapcenter.replace('[',''); mapcenter = mapcenter.replace(']','');
 mapcenter = mapcenter.replace(" ",'');
  
 attraction_list = str(the_result); attraction_list = attraction_list.replace("'","") 
 attraction_list = attraction_list[1:-1]; attraction_list = " "+attraction_list

   
 attraction_desc = str(attraction_desc); attraction_desc = attraction_desc.replace("'","") 
 attraction_desc = attraction_desc[1:-1]; attraction_desc = " "+attraction_desc
  
  
 allmypics = str(attraction_list_names);allmypics = allmypics.replace("'","");allmypics = allmypics[1:-1];  
 attraction_dur = str(attraction_dur);attraction_dur = attraction_dur.replace("'","");attraction_dur = attraction_dur[1:-1];   
 attraction_start = str(attraction_start);attraction_start = attraction_start.replace("'","");attraction_start = attraction_start[1:-1];   
 
 plinepath = np.asarray(latmat);
 plinepath = [list(a) for a in zip(plinepath[:,0],plinepath[:,1])]
 fin_latlons.append((0,0));
 print fin_latlons
 fin_latlons = str(fin_latlons); fin_latlons = fin_latlons.replace('(','');
 fin_latlons = fin_latlons.replace(')','')

 
 user_features = str(user_features); 
 user_features = user_features[2:-2]; 
 user_features = user_features.replace("'",'')
 
 return render_template("output.html",attraction_list=attraction_list,allmypics = allmypics,user_features=user_features,fin_latlons=fin_latlons,attraction_desc=attraction_desc,mapcenter = mapcenter,attraction_dur = attraction_dur,attraction_start = attraction_start, plinepath=plinepath)

   


