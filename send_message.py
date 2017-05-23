from twilio.rest import Client
from twilio_credentials import account_sid, auth_token, number_from, number_to

client = Client(account_sid, auth_token)

def send_message(text):
	# message = client.messages.create(
	# 	to=number_to, 
	# 	from_=number_from,
	# 	body=text)
	# print(message.sid)
	print "message sent --> "+text