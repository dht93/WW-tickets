import requests
from bs4 import BeautifulSoup
from send_message import send_message
# import urllib2


MESSAGE = "Wonder Woman booking is live!!"

#scrape1 scrapes the movie listing page for a specific multiplex
def scrape1(url):
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
			found = check_for_keyword(movie_name)
			if found == True:
				break
		except Exception:
			pass

#scrape2 scrapes the all english movies page
def scrape2(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	tags = soup.find_all("div",class_="wow fadeIn movie-card-container")
	for el in tags:
		try:
			movie_name = el.contents[1].contents[1].contents[1].contents[1]['alt'].lower()
			found = check_for_keyword(movie_name)
			if found == True:
				break
		except Exception:
			pass


def check_for_keyword(keyword):
	print keyword
	if "wonder woman" in keyword or "wonder" in keyword or "woman" in keyword:
		send_message(MESSAGE)
		return True
	else:
		# print "no cigar"
		return False
