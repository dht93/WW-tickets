from flask import Flask, redirect, request
app = Flask(__name__)
app.config['DEBUG'] = True
import datetime
from scrapeBMS import scrape1, scrape2
from google.cloud import logging

base_url = "https://in.bookmyshow.com/buytickets/prasads-hyderabad/cinema-hyd-PRHN-MT/"

all_english_url = "https://in.bookmyshow.com/hyderabad/movies/english"

CHECK_FOR_DAYS = 5

def get_time_stamp_value(increment=0):
	date = datetime.datetime.now().date()
	if increment!=0:
		date+=datetime.timedelta(days=increment)
	month = "%02d" % date.month
	day = "%02d" % date.day
	timestamp_val = str(date.year) + month + day
	return timestamp_val

@app.route('/')
def hello():
	return 'WW!'

@app.route('/tasks/check-for-WW')
def cron():
	#check for all english movies listing
	scrape2(all_english_url)

	#check for the next few days at Prasads
	for i in range(CHECK_FOR_DAYS):
		date = get_time_stamp_value(i)
		url = base_url+date
		print url
		scrape1(url)
	return '200 OK',200

@app.errorhandler(404)
def page_not_found(e):
	return 'Sorry, nothing at this URL.', 404
