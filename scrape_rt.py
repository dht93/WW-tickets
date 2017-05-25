import requests
from bs4 import BeautifulSoup
from send_message import send_message
from other_server_urls import UPDATE_RT

MESSAGE = "Wonder Woman RT score out!"


def update_rt_sent():
	r = requests.get(UPDATE_RT)

def check_for_score(url):

	r = requests.get(url)
	html = r.text

	soup = BeautifulSoup(html, 'html.parser')
	try:
		score_panel = soup.find("div",id="scorePanel")
		proceed = True
	except Exception:
		proceed = False

	if proceed == True:

		try:
			meter = score_panel.find("span",class_="meter-value")
			score = meter.contents[0].contents[0].strip()
		except Exception:
			score = None
			print "Score not yet out"
		if score != None:
			send_message(MESSAGE)
			update_rt_sent()