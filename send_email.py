from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from make_cover_letters import *
from credentials import *
import inspect




def send_email(profile, 
			job_type,
			contact,
			job,
			office, 
			company,
			name, 
			title, 
			school, 
			phone, 
			gmail_user,
			gmail_pass,
			contact_email
			):
	
	
	subject = "{} Position - {}".format(job, company)

	#msg = MIMEMultipart()
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = (name)
	msg['To'] = (contact_email)
	

	# That is what u see if dont have an email reader:
	msg.preamble = ''
	#print(msg.preamble)

	#Message (Text Version & HTML Version)
	message_output = make_html_text_cl(
		profile, 
		job_type, 
		contact, 
		job, 
		office, 
		company, 
		name, 
		title, 
		school, 
		phone, 
		gmail_user
		)



	text = MIMEText(message_output[0], 'plain')
	html = MIMEText(message_output[1], 'html')
	internships = message_output[2]

	msg.attach(text)
	msg.attach(html)

	#TODO
	#Insert Write Resume Code

	#Resume
	resume_filename = "Resume_{}.pdf".format(name.replace(' ', '_'))
	resume_path = "{}/{}/{}".format(profile, job_type, resume_filename)

	#Attach Resume
	part = MIMEApplication(open(resume_path,"rb").read())
	part.add_header('Content-Disposition', 'attachment', filename=resume_filename)
	msg.attach(part)
	#print(msg)
	#print("[*] composing email message to {} - {} | {}".format(contact, contact_email, subject))

	#Print Metadata
	txt = message_output[0]
	snip = "{}...{}".format(txt[0:35], txt[-40:]).replace('\n', '')
	meta = inspect.cleandoc("""
					Subject : {}
					From : {}
					To : {}
					Attachment: {}
					Text: {}
			""".format(	msg['Subject'], 
						msg['From'], 
						msg['To'], 
						resume_path, 
						snip))

	#print(meta)


	# Create an instance in SMTP server
	smtp = SMTP("smtp.gmail.com:587")
	smtp.ehlo()
	smtp.starttls()
	smtp.login(gmail_user, gmail_pass)

	# Send the email
	smtp.sendmail(msg.get('From'),msg["To"],msg.as_string())
	smtp.quit()


	return meta.replace('\n', '|')

#message("P05RH", "data_science", contact, job, office, company, name, title, school, phone, gmail_user, gmail_pass, contact_email)
