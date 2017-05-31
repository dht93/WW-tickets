import sendgrid
from sendgrid.helpers.mail import *
from sendgrid_key import from_email, to_email

def send_email(key,subject,message):
	try:
		message = message
		sg = sendgrid.SendGridAPIClient(apikey=key)	
		from_email1 = Email(from_email)
		to_email1 = Email(to_email)
		subject = subject
		content = Content("text/html", message)
		mail = Mail(from_email1, subject, to_email1, content)
		response = sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print str(e)