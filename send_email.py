from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from make_cover_letters import *
from make_resumes import *
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
			school_ctyst,
			school_cszip,
			school_address,
			department,
			ba_school, 
			ba_ctyst,
			internship1,
			int1_ctyst,
			internship2,
			int2_ctyst,
			treatment,
			phone, 
			gmail_user,
			gmail_pass,
			contact_email,
			pair_version
			):
	
	
	#TODO Pass "Pair" to Email
	#Need alt style for a number of elements in the email,
	#such as the resume style, cover_letter style, subject line,
	#signature, etc

	#To avoid confounding whether one 'style' is better or worse
	#with partisan or non-partisan, the 'style' needs to be randomized
	#as well.

	#By passing the pair 'a' or 'b' to the send_email 
	#func, any style element can have at random an a and b version

	if pair_version == 'A':
		subject = "{} Position - {}".format(job, company)
	elif pair_version == 'B':
		subject = "{} - {} Position".format(company, job)

	msgRoot = MIMEMultipart('mixed')
	msgRoot['Subject'] = subject
	msgRoot['From'] = name
	msgRoot['To'] = contact_email
	msgRoot.preamble = ''
	

	#Create alternative portion to allow adding 
	#both plain and HTML versions of the cover letter
	msgAlt = MIMEMultipart('alternative')
	msgRoot.attach(msgAlt)

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
		department,
		internship1,
		int1_ctyst,
		internship2,
		int2_ctyst,
		treatment, 
		phone, 
		gmail_user
		)



	text = MIMEText(message_output[0], 'plain')
	html = MIMEText(message_output[1], 'html')

	#Insert Message Cover Letter
	msgAlt.attach(text)
	msgAlt.attach(html)

	#Write Resume Code
	make_resume(profile,
				job_type,
				name, 
				phone,
				gmail_user,
				school, 
				school_ctyst,
				school_cszip,
				school_address,
				department,
				ba_school, 
				ba_ctyst, 
				internship1,
				int1_ctyst,
				internship2,
				int2_ctyst,
				treatment,
				pair_version)

	#Resume
	resume_filename = "Resume_{}.pdf".format(name.replace(' ', '_'))
	resume_path = "{}/{}/tex/{}".format(profile, job_type, resume_filename)

	#Attach Resume
	part = MIMEApplication(open(resume_path,"rb").read())
	part.add_header('Content-Disposition', 'attachment', filename=resume_filename)
	msgRoot.attach(part)

	#Print Metadata
	txt = message_output[0]
	snip = "{}...{}".format(txt[0:35], txt[-40:]).replace('\n', '')

	meta = inspect.cleandoc("""
					Subject : {}
					From : {}
					To : {}
					Attachment: {}
					Text: {}
			""".format(	msgRoot['Subject'], 
						msgRoot['From'], 
						msgRoot['To'], 
						resume_path, 
						snip))



	# Create an instance in SMTP server
	smtp = SMTP("smtp.gmail.com:587")
	smtp.ehlo()
	smtp.starttls()
	smtp.login(gmail_user, gmail_pass)

	# Send the email
	smtp.sendmail(msgRoot['From'], msgRoot["To"], msgRoot.as_string())
	smtp.quit()


	return meta.replace('\n', '|')


