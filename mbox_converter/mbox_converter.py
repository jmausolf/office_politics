import mailbox
import csv
import re
import sys
import subprocess
import argparse
from glob import glob
import pandas as pd
from bs4 import BeautifulSoup
from email_reply_parser import EmailReplyParser
from profile_dict import *



#######################################
## MBOX LOADING
#######################################


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)


def rm_email_punct(text):
    tmp = re.sub(r'[]\\?!\"\'+*/`\\[<=>\\^]', "", text)
    return re.sub(r'\s{2,}', " ", tmp)
    #return text


def replace_soup_tags(text):
	text = text.replace("&gt;", "")
	text = text.replace("&lt;", "")
	return text

def replace_unicode_literals(text):
	text = text.replace("\\xe2\\x80\\x90", "-")
	text = text.replace("\\xe2\\x80\\x91", "-")
	text = text.replace("\\xe2\\x80\\x92", "-")
	text = text.replace("\\xe2\\x80\\x93", "-")
	text = text.replace("\\xe2\\x80\\x94", "-")
	text = text.replace("\\xe2\\x80\\x98", "'")
	text = text.replace("\\xe2\\x80\\x99", "'")
	text = text.replace("\\xe2\\x80\\x9a", "'")
	text = text.replace("\\xe2\\x80\\x9b", "'")
	text = text.replace("\\xe2\\x80\\x9c", '"')
	text = text.replace("\\xe2\\x80\\x9d", '"')
	text = text.replace("\\xc2\\xa0", ' ')
	return text


def replace_links(link_text):
	link = re.sub(r'<[^>]+>', ' ', link_text)
	return re.sub(r'\s{2,}', ' ', link)
	#link = re.sub(r'\<.*?\>', '[link]', link_text)
	#return link


def rm_history(message):
	m = message

	try:
		m = m.split('From: ')[0]
	except:
		pass
	try:
		m = m.split('*From:*')[0]
	except:
		pass
	try:
		m = m.split('On ')[0]
	except:
		pass

	return m



def more_payloads(message):
	body = ""
	if message.is_multipart():
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		if message.get_content_type() == 'text/plain':
			body = message.get_payload(decode=True)
		elif message.get_content_type() == 'text/html':
			body = message.get_payload(decode=True)
		else:
			#import pdb; pdb.set_trace()
			#'application/octet-stream'
			#'text/html'
			pass

	

	#Remove HTML/CSS
	soup = BeautifulSoup(body, "html5lib")
	[s.extract() for s in soup('style')]
	o = EmailReplyParser.parse_reply(str(soup))
	o = remove_non_ascii_2(str(o))

	#Remove GT/LT Tags
	o = replace_soup_tags(o)

	#o = remove_non_ascii_2(str(body))
	o = "\n".join(o.splitlines())
	o = o.replace("\\r\\n", "\n")
	o = o.replace("\\n\\n", "\n").replace("\\n", "\n")
	o = o.replace("\b'", '').replace("b'", '')
	o = replace_unicode_literals(o)

	#Remove Additional Reply History
	o = rm_history(o)
	o = '''{}'''.format(replace_links(o))


	if len(o) > 20000:
		return o[0:20000]
	else:
		return o


def clean_subject(subject):

	o = remove_non_ascii_2(str(subject))
	o = "\n".join(o.splitlines())
	o = o.replace("\\r\\n", "\n")
	o = o.replace("\\n\\n", "\n").replace("\\n", "\n")
	o = o.replace("\b'", '').replace("b'", '')
	o = replace_unicode_literals(o)
	o = '''{}'''.format(replace_links(o))

	if len(o) > 500:
		return o[0:500]
	else:
		return o


def get_recipient(message):

	to_text = message['to']
	try:
		terms = to_text.split(' <')
		to_name = rm_email_punct(terms[0])
		to_email = rm_email_punct(terms[1])
	except:
		try:
			to_email = rm_email_punct(to_text)
			to_name = to_email
		except:
			to_email = to_text
			to_name = to_email

	return to_name, to_email


def get_sender(message):
	'''
	Expects message from mbox
	Returns sender name and email
	'''
	#print(message)
	from_text = message['from']
	#print(from_text)
	try:
		terms = from_text.split(' <')
		from_name = rm_email_punct(terms[0])
		from_email = rm_email_punct(terms[1])
	except:
		try:
			from_email = rm_email_punct(from_text)
			from_name = from_email
		except:
			from_email = from_text
			from_name = from_email

	return from_name, from_email


def get_message_id(message):

	mid = message['message-id']
	mid = mid.split('<')[1].split('>')[0]
	return mid


def mbox_extractor(mboxfile, writer):
	print("[*] extracting emails from mbox: {}...".format(mboxfile))
	for message in mailbox.mbox(mboxfile):
			
		from_name, from_email = get_sender(message)
		to_name, to_email = get_recipient(message)
		body = more_payloads(message)
		subject = clean_subject(message['subject'])
		message_id = get_message_id(message)
		writer.writerow([
						from_name,
						from_email, 
						to_name,
						to_email,
						message['date'], 
						subject,
						message['x-gmail-labels'],
						body,
						message_id,
						mboxfile
						])


def csv_from_mboxes(filename='mbox.csv'):

	with open(filename, "w") as outfile:
		writer = csv.writer(outfile)
		cols = ['from_name',
				'from_email',
				'to_name',
				'to_email',
				'date',
				'subject',
				'labels', 
				'message',
				'message_id',
				'mbox']
		writer.writerow(cols)


		mboxes = glob('*.mbox')
		for m in mboxes:
			mbox_extractor(m, writer)



#######################################
## MBOX CLEANING
#######################################

#####################################
##your message to

##TODO
##need code to extract from the messages the email address following
## 'your message to' 
## and create a new row with certain properties
## to artificially create the 'sent' data


def extract_email(message):
	try:
		match = re.search(r'[\w\.-]+@[\w\.-]+', message)
		email = match.group(0)
	except:
		email = None

	if email is not None:
		if email[-1:] == '.':
			email = email[:-1]
		else:
			pass
		#print(email)
		#print(email[-1:])

	return email


#bounce types seen
#type 1: sent is True
	#keep as is

#type 2: sent is False
	#extacted email exists != profile sender
	#join these with sent mbox
	#df1 = filter from bounces
	#df2 = filter from sent
	#join

#other type is sent is False but equals profile email

#append type 1 and type 2, need to keep unique to_email
#join with protocol (deduped by to_email) to get a list of firms to resent
#(after getting new emails/jobs)

def get_disjoint_bounces(df_bounce):
	pass


def isprofile(email):

	if email in profile_emails:
		return True
	else:
		return False

def filter_bounces_main(df):

	print(profile_emails)

	#Filter Profile
	#df = df.loc[(df['profile'] == 'P04NL')]

	#Get Bounces DF
	df = df.loc[(df['outcome'] == 'Bounce')].copy()
	df['extracted_email'] = df['message'].apply(extract_email)
	df['isprofile'] = df['extracted_email'].apply(isprofile)

	df.to_csv("bounce_test1.csv")

	#Get Type 1
	type_1_crit = 	(
						(df['outcome'] == 'Bounce') &
						(df['sent'] == True)	

					)

	df_type_1 = df.loc[type_1_crit].copy()
	df_type_1 = df_type_1.drop(['extracted_email', 'isprofile'], axis=1)
	df_type_1['bounce_email'] = df_type_1['to_email']
	bounce_1 = df_type_1['bounce_email']


	#Get Type 2
	type_2_crit = 	(
						(df['outcome'] == 'Bounce') &
						(df['sent'] == False) &
						(df['isprofile'] == False) 

					)
	df_type_2 = df.loc[type_2_crit].copy().dropna()
	df_type_2 = df_type_2.drop_duplicates(subset=['extracted_email'])
	df_type_2['bounce_email'] = df_type_2['extracted_email']
	bounce_2 = df_type_2['bounce_email']


	#Get Type 3
	type_3_crit = 	(
						(df['outcome'] == 'Bounce') &
						(df['sent'] == False) &
						(df['isprofile'] == False) 

					)
	df_type_3 = df.loc[type_3_crit].copy().dropna()
	df_type_3 = df_type_3
	df_type_3['bounce_email'] = df_type_3['from_email']
	bounce_3 = df_type_3['bounce_email']


	#Append Bounce Type Emails
	bounces = pd.concat([bounce_1, bounce_2, bounce_3]).sort_values().to_frame()
	gb = ['bounce_email']
	bounces['count'] = bounces.groupby(gb)['bounce_email'].transform('count')
	bounces = bounces.sort_values(['count'])
	bounces = bounces.drop_duplicates()

	#Remove Profile Emails and Save
	bounces['isprofile'] = bounces['bounce_email'].apply(isprofile)
	bounces = bounces.loc[(bounces['isprofile'] == False)]
	bounces.drop(['isprofile'], axis=1, inplace=True)
	bounces.to_csv("bounce_emails_W1.csv", index=False)
	print(bounces)



def modify_main_mbox_csv(filename='mbox.csv'):

	df = pd.read_csv(filename)

	#Parse Profile, Wave, and Outcome from Mbox Filename
	tmp = df['mbox'].apply(lambda x: x.replace('-', '_').split('.mbox')[0])
	tmp = tmp.str.split('_', n = 2, expand = True)
	df['profile'], df['wave'], df['outcome'] = tmp[0], tmp[1], tmp[2]


	#Parse Sent from Labels
	#df['sent'] = False
	#sent_crit = (df['labels'].str.contains(r'[sS]ent'))
	#df.loc[sent_crit, 'sent'] = True

	#Determine if Profile Sent Email
	df['sent'] = df['from_email'].apply(profile_sender, profiles_list=profile_emails)

	#Remove Sent Emails
	df = df.loc[df['sent'] != True]
	df = df.loc[df['outcome'] != 'Sent']


	#Create an Mbox Email for Matching with Protocol
	df['mbox_email'] = df['mbox'].apply(ret_mbox_email)

	#TODO
	#Make method of callback cols


	#TODO
	#filter bounces with different protocols from types


	print(df)
	print(df.columns)

	#Write Results
	outfile = filename.split('.csv')[0]+'_analysis.csv'
	df.to_csv(outfile, index=False)
	#print(tmp)
	return df





def modify_main():
	df = modify_main_mbox_csv(args.filename)

	filter_bounces_main(df)

			
if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", 
						"--filename",
						default='mbox.csv',
						type=str, 
						help="outfile name")
	parser.add_argument("-o", 
						"--open",
						default=False,
						type=bool, 
						help="open outfile?")
	parser.add_argument("-l", 
						"--load",
						default=False,
						type=bool, 
						help="load mbox files")
	parser.add_argument("-m", 
						"--modify",
						default=False,
						type=bool, 
						help="modify mbox csv")
	args = parser.parse_args()

	if not (args.load or args.modify):
		parser.error('No action requested, add argument...')

	if args.load is True:
		print("[*] Running requested tasks...")
		csv_from_mboxes(args.filename)
		print(pd.read_csv(args.filename))
		print(pd.read_csv(args.filename).isna().sum())
		if args.open is True:
			subprocess.call("open {}".format(args.filename), shell=True)
		print("[*] Done.")
	

	if args.modify is True:

		#Working on Editing Mbox
		#modify_mbox_csv(args.filename)
		modify_main()

		if args.open is True:
			subprocess.call("open {}".format(args.filename), shell=True)
		print("[*] Done.")