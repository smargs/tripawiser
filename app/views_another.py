from flask import render_template, request
from app import app
import pymysql as mdb
from a_Model import ModelIt
import pickle

#import requests
#start = requests.args.get('start')

homeurl = '/home/smargs/Dropbox/Push/insight_project/ta_reviews/'
 
with open(homeurl+'all_attractions_info_new.pickle') as f:
    attraction_info,attraction_title,attraction_type,attraction_typer,attraction_address,attraction_latlon,attraction_opentime,attraction_closetime,attraction_ratings,attraction_review_count = pickle.load(f) 
    

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

@app.route('/input')
def cities_input():
  return render_template("input.html")
 

@app.route('/output')
def cities_output():
  #pull 'ID' from input field and store it
  interest = request.args.get('ID')
 

  all_interests = []; all_interests.append(interest)

  #call a function from a_Model package. note we are only pulling one result in the query
  #pop_input = cities[0]['population']
 
  the_result = [];
  for i,j in enumerate(all_interests):
      the_result.extend(attraction_typer[j])
  
 
  
   
      
  return render_template("output.html", cities = all_interests, the_result = the_result)

   


