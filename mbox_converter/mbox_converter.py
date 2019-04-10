import mailbox
import csv
import re
import sys
import subprocess
import argparse
from glob import glob
import pandas as pd


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)


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
	return text


def replace_links(link_text):
	link = re.sub(r'\<.*?\>', '[link]', link_text)
	return link


def more_payloads(message):
	body = ""
	if message.is_multipart():
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		if message.get_content_type() == 'text/plain':
			body = message.get_payload(decode=True)


	o = remove_non_ascii_2(str(body))
	o = "\n".join(o.splitlines())
	o = o.replace("\\r\\n", "\n")
	o = o.replace("\\n\\n", "\n").replace("\\n", "\n")
	o = o.replace("\b'", '').replace("b'", '')
	o = replace_unicode_literals(o)
	o = replace_links(o)
	return o


def get_sender(message):
	'''
	Expects message from mbox
	Returns sender name and email
	'''

	from_text = message['from']
	terms = from_text.split(' <')
	from_name = terms[0]
	from_email = terms[1].replace('>', '')

	return from_name, from_email


def mbox_extractor(mboxfile, writer):
	print("[*] extracting emails from mbox: {}...".format(mboxfile))
	for message in mailbox.mbox(mboxfile):
			
		from_name, from_email = get_sender(message)
		body = more_payloads(message)
		writer.writerow([
						from_name,
						from_email, 
						message['to'], 
						message['date'], 
						message['subject'],
						message['x-gmail-labels'],
						body,
						mboxfile
						])


def csv_from_mboxes(filename='mbox.csv'):

	with open(filename, "w") as outfile:
		writer = csv.writer(outfile)
		cols = ['from_name',
				'from_email',
				'to_email',
				'date',
				'subject',
				'labels', 
				'message',
				'mbox']
		writer.writerow(cols)


		mboxes = glob('*.mbox')
		for m in mboxes:
			mbox_extractor(m, writer)



			
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
	args = parser.parse_args()

	if not (args.filename or args.open):
	    parser.error('No action requested, add argument...')


	print("[*] Running requested tasks...")
	csv_from_mboxes(args.filename)
	print(pd.read_csv(args.filename))
	if args.open is True:
		subprocess.call("open {}".format(args.filename), shell=True)
	print("[*] Done.")

