import requests
from bs4 import BeautifulSoup
from send_message import send_message
# import urllib2
from other_server_urls import UPDATE_BMS
from send_email import send_email
from sendgrid_key import key


MESSAGE = "Wonder Woman booking is live!!"

email_subject = "Wonder Woman BookMyShow"
email_msg = "<h1>Wonder Woman booking on BookMyShow is live now!!</h1>"

def update_bms_sent():
	r = requests.get(UPDATE_BMS)

def send_notifications():
	#try sending success mail
	try:
		send_email(key,email_subject,email_msg)
	except Exception as e:
		print "Email not sent"
		print str(e)

	message_sent = False

	#try sending success message
	try:
		send_message(MESSAGE)
		message_sent = True
	except Exception as e:
		print str(e)

	if message_sent == True:
		#try updating bms_sent
		try:
			update_bms_sent()
		except Exception as e:
			print str(e)


#scrape1 scrapes the movie listing page for a specific multiplex
def scrape1(url, word_list):
	r = requests.get(url)
	# resp = urllib2.urlopen(url)
	# html = resp.read()
	html = r.text

	soup = BeautifulSoup(html, 'html.parser')

	tags = soup.find_all(class_="__name")

	# ww = False
	for el in tags:
		try:
			movie_name = el.contents[1].contents[0].lower()
			found = check_for_keyword(movie_name, word_list)
			if found == True:
				send_notifications()
				return True
		except Exception:
			pass
	return False

#scrape2 scrapes the all english movies page
def scrape2(url, word_list):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	tags = soup.find_all("div",class_="wow fadeIn movie-card-container")
	for el in tags:
		try:
			movie_name = el.contents[1].contents[1].contents[1].contents[1]['alt'].lower()
			found = check_for_keyword(movie_name, word_list)
			if found == True:
				send_notifications()
				break
		except Exception:
			pass


def check_for_keyword(keyword, word_list):
	print keyword
	for word in word_list:
		if word in keyword:
			#BMS booking live!
			return True
	return False
