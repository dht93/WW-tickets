from flask import Flask, redirect, request
app = Flask(__name__)
app.config['DEBUG'] = True
import datetime
from scrapeBMS import scrape1, scrape2
from scrape_rt import check_for_score
from google.cloud import logging

logging_client = logging.Client()
logger = logging_client.logger("tracker")

def log(params):
	logger.log_struct(params)


base_url = "https://in.bookmyshow.com/buytickets/prasads-hyderabad/cinema-hyd-PRHN-MT/"

all_english_url = "https://in.bookmyshow.com/hyderabad/movies/english"

rt_url = "https://www.rottentomatoes.com/m/wonder_woman_2017"

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
		# print url
		scrape1(url)
	return '200 OK',200

@app.route('/tasks/check-for-rt-score')
def rt_score_cron():
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
