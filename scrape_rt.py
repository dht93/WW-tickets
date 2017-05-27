import requests
from bs4 import BeautifulSoup
from send_message import send_message
from other_server_urls import UPDATE_RT
from send_email import send_email
from sendgrid_key import key

MESSAGE = "Wonder Woman RT score out!"

email_subject = "Wonder Woman RT Score"
email_msg = "<h1>Wonder Woman RT score live now!!</h1>"

def update_rt_sent():
	r = requests.get(UPDATE_RT)

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
		#try updating rt_sent
		try:
			update_rt_sent()
		except Exception as e:
			print str(e)

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
			#score out!
			send_notifications()
