from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from credentials import *
from messages import *



job = "Data Scientist"
company = "Google"
subject = "{} Position - {}".format(job, company)

msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = ('Matthew Zachary Hartman')
msg['To'] = (to_contact)

# That is what u see if dont have an email reader:
msg.preamble = ''
print(msg.preamble)

# This is the textual part:
message_body = MIMEText(message_text)
msg.attach(message_body)

#part1 = MIMEText(sig_text, 'plain')
part2 = MIMEText(sig_html, 'html')

#msg.attach(part1)
msg.attach(part2)


# This is the binary part(The Attachment):
part = MIMEApplication(open("Resume_Matthew_Zachary_Hartman.pdf","rb").read())
part.add_header('Content-Disposition', 'attachment', filename="file.pdf")
msg.attach(part)
print(msg)



# Create an instance in SMTP server
smtp = SMTP("smtp.gmail.com:587")
smtp.ehlo()
smtp.starttls()
smtp.login(gmail_user, gmail_pass)

# Send the email
smtp.sendmail(msg.get('From'),msg["To"],msg.as_string())
smtp.quit()

