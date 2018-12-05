import random
import pandas as pd
#from new_messages import *
from cover_letters import *
import textwrap
import inspect
import textile


def keep_or_replace(app_company, intern_company):

	if app_company == intern_company:
		return "REPLACE"
	else:
		return "KEEP"


def sub_cover_letter_internship(app_company, job_type_prestige):
	
	d = job_type_prestige.copy()
	#print(d)
	try:
		del d[app_company]
	except:
		pass

	#intern companies
	ics = []

	for i in range(0, 2):
		ic = random.choice(list(d.items()))[0]
		ics.append(ic)
		del d[ic]


	ic_phrase = "{} and {}".format(ics[0], ics[1])
	return ic_phrase


def make_text_sig(name, title, school, phone, gmail_user):

	#Correct 'the' case in Universities
	school = school.replace('the', 'The', 1)

	sig_text = inspect.cleandoc("""

		{0}
		{1}
		{2}
		C: {3} | {4}
	""".format(name, title, school, phone, gmail_user))

	return sig_text

def make_html_sig(name, title, school, phone, gmail_user, rgb, pair_version):

	#Correct 'the' case in Universities
	school = school.replace('the', 'The', 1)

	phone_link = "+1{}".format(phone.replace('-', ''))

	if pair_version == 'A':
		sig_html = """
		<div style="background-color:rgb(255,255,255)"><font face="Garamond" size="3">{0}</font>
		</div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Garamond">{1}</font>
		</div>
		<div style="font-family:Tahoma;font-size:13px"><font face="Garamond" size="3" style="background-color:rgb(255,255,255);color:rgb({6})"><b>{2}</b></font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Garamond">M:<span>&nbsp;</span><a href="tel:{3}" value="{4}" style="color:rgb(17,131,204)" target="_blank">{3}</a><span>&nbsp;</span>|<span>&nbsp;</span><a href="mailto:{5}" class="m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560m_2319474238175162055dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734dly-gmail m_-4756129822142185649gmail-m_4655728448235344902dly-gmail m_-4756129822142185649gmail-dly-gmail m_-4756129822142185649dly-gmail dly-gmail" style="color:rgb(17,131,204)" target="_blank">{5}</a></font></div></div>
		""".format(name, title, school, phone, phone_link, gmail_user, rgb)

	elif pair_version == 'B':
		sig_html = """
		<div style="background-color:rgb(255,255,255)"><font face="Palatino" size="3">{0}</font>
		</div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Palatino">{1}</font>
		</div>
		<div style="font-family:Tahoma;font-size:13px"><font face="Copperplate" size="3" style="background-color:rgb(255,255,255);color:rgb({6})">{2}</font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Palatino">C:<span>&nbsp;</span><a href="tel:{3}" value="{4}" style="color:rgb(17,85,204)" target="_blank">{3}</a><span>&nbsp;</span>|<span>&nbsp;</span><a href="mailto:{5}" class="m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560m_2319474238175162055dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734dly-gmail m_-4756129822142185649gmail-m_4655728448235344902dly-gmail m_-4756129822142185649gmail-dly-gmail m_-4756129822142185649dly-gmail dly-gmail" style="color:rgb(17,85,204)" target="_blank">{5}</a></font></div></div>
		""".format(name, title, school, phone, phone_link, gmail_user, rgb)

	return sig_html


def make_text_cl(profile, 
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
				gmail_user,
				pair_version,
				add_sig=True
				):

	internships = "{} and {}".format(internship1, internship2)

	#Select Partisan or Neutral Cover Letter for Job Type
	#if profile == 'P03NH' or profile == 'P04NL':
	#	method_name = "{}_{}".format('neutral', job_type)
	#else:
	#	method_name = "{}_{}".format('partisan', job_type)

	#Select Version of Cover Letter for Job Type
	method_name = "{}_{}".format(job_type, pair_version)

	my_cls = cl()
	cl_text = None
	try:
		cl_text = getattr(cl(), method_name)
	except AttributeError:
		raise NotImplementedError("Class `{}` does not implement `{}`"
			.format(cl().__class__.__name__, method_name))

	message_body = cl_text(contact, job, office, company, 
						   internships, school, department, treatment)

	if add_sig is True:
		message_sig = make_text_sig(name, title, school, phone, gmail_user)
		message_text = message_body+'\n\n'+message_sig
	else:
		message_text = message_body

	return message_text


def make_html_text_cl(profile, 
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
				gmail_user,
				rgb,
				pair_version
				):

	#Make Text CL (no sig)
	message_text_body = make_text_cl(profile, 
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
								  gmail_user,
								  pair_version,
								  add_sig=False)

	#Make Text Sig/Full Text Message
	sig_text = make_text_sig(name, title, school,
							 phone, gmail_user)
	message_text = message_text_body+'\n\n'+sig_text

	#Make HTML Sig
	sig_html = make_html_sig(name, title, school,
							 phone, gmail_user, rgb, pair_version)

	#Make HTML Message from Text CL and HTML Sig
	#(needed to keep the internships consistent)
	if pair_version == 'A':
		message_html = """<html><div style="color:rgb(0,0,0);font-family:&quot;Times New Roman&quot;,Times,serif,Times,EmojiFont,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;,NotoColorEmoji,&quot;Segoe UI Symbol&quot;,&quot;Android Emoji&quot;,EmojiSymbols;font-size:16px;font-style:normal;font-variant-ligatures:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;background-color:rgb(255,255,255);text-decoration-style:initial;text-decoration-color:initial"><font face="Garamond">{}\n\n{}</div></html>
		""".format(textile.textile( message_text_body ), sig_html)
	elif pair_version == 'B':
		message_html = """<html><div style="color:rgb(0,0,0);font-family:&quot;Times New Roman&quot;,Times,serif,Times,EmojiFont,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;,NotoColorEmoji,&quot;Segoe UI Symbol&quot;,&quot;Android Emoji&quot;,EmojiSymbols;font-size:16px;font-style:normal;font-variant-ligatures:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;background-color:rgb(255,255,255);text-decoration-style:initial;text-decoration-color:initial"><font face="Palatino">{}\n\n{}</div></html>
		""".format(textile.textile( message_text_body ), sig_html)

	return message_text, message_html

#join_experiment_profiles("experiment_test.csv")


