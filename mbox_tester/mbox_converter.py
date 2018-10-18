# assumes your file is called mbox (which it is if you export from Mac Mail)
# writes to a file called mbox.csv

import mailbox
import csv
import re

def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)


def replace_links(link_text):
	link = re.sub(r'\<.*?\>', '[link]', link_text)
	return link


# motherfucking recursion, because email is damn weird.
# each payload can contain many other payloads, which can contain many *other* payloads
# this only exports the text/plain payload, the thing you read
def more_payloads(message):
	body = ""
	if message.is_multipart():
		print("if")
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		print("else")
		if message.get_content_type() == 'text/plain':
			body = message.get_payload(decode=True)

	output = remove_non_ascii_2(str(body))
	output = "\n".join(output.splitlines())
	output = output.replace("\\r\\n", "\n").replace("\\n\\n", "\n")
	output = output.replace('\b"', '')
	output = replace_links(output)
	#print(output)
	return output

with open("mbox.csv", "w") as outfile:
	writer = csv.writer(outfile)
	for message in mailbox.mbox('Inbox.mbox'):
		body = more_payloads(message)
		writer.writerow([message['subject'], message['from'], message['date'], body])