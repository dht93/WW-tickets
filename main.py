from flask import Flask, redirect, request
app = Flask(__name__)
app.config['DEBUG'] = True
import datetime
from scrapeBMS import scrape1, scrape2
from scrape_rt import check_for_score
from google.cloud import logging
import requests
from other_server_urls import GET_STATUS

logging_client = logging.Client()
logger = logging_client.logger("tracker")

def log(params):
	logger.log_struct(params)


base_url = "https://in.bookmyshow.com/buytickets/prasads-hyderabad/cinema-hyd-PRHN-MT/"
base_url_big_screen = "https://in.bookmyshow.com/buytickets/prasads-large-screen/cinema-hyd-PRHY-MT/"
all_english_url = "https://in.bookmyshow.com/hyderabad/movies/english"

rt_url = "https://www.rottentomatoes.com/m/wonder_woman_2017"

CHECK_FOR_DAYS = 2

word_list = ["wonder woman", "wonder", "woman"]

#make this reusable
release_date = datetime.datetime(2017,6,2)

def get_time_stamp_value(increment=0):
	# date = datetime.datetime.now().date()
	date = release_date
	if increment!=0:
		date+=datetime.timedelta(days=increment)
	month = "%02d" % date.month
	day = "%02d" % date.day
	timestamp_val = str(date.year) + month + day
	return timestamp_val

def get_status():
	r = requests.get(GET_STATUS)
	print r.text
	resp = r.text
	resp = resp.strip().split(",")
	bms_sent = resp[0]
	rt_sent = resp[1]
	return bms_sent,rt_sent


@app.route('/')
def hello():
	return 'WW!'

@app.route('/tasks/check-for-WW')
def cron():
	bms_sent,rt_sent = get_status()
	if bms_sent == "0":
		print "message not yet sent"
		#check for all english movies listing
		scrape2(all_english_url, word_list)

	bms_sent,rt_sent = get_status()	
	#check for the next few days at Prasads
	if bms_sent == "0":
		for i in range(CHECK_FOR_DAYS):
			date = get_time_stamp_value(i)
			url = base_url+date
			# print url
			found = scrape1(url, word_list)
			if found == True:
				break

	bms_sent,rt_sent = get_status()	
	#check for the next few days at Prasads Big Screen
	if bms_sent == "0":
		for i in range(CHECK_FOR_DAYS):
			date = get_time_stamp_value(i)
			url = base_url_big_screen+date
			# print url
			found = scrape1(url, word_list)
			if found == True:
				break

	return '200 OK',200

@app.route('/tasks/check-for-rt-score')
def rt_score_cron():
	bms_sent,rt_sent = get_status()
	if rt_sent=="0":
		print "message not yet sent"
		check_for_score(rt_url)
	return '200 OK',200


@app.route('/redirect-to-repo')
def redirect_to_repo():
	params = {'user-agent':request.headers.get('User-Agent'),
			'ip-address':request.remote_addr}
	log(params)
	return redirect("https://github.com/dht93/WW-tickets")

@app.errorhandler(404)
def page_not_found(e):
	return 'Sorry, nothing at this URL.', 404
