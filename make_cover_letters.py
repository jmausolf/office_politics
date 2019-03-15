import random
import pandas as pd
from cover_letters import *
import textwrap
import inspect
import textile
import re


def remove_punct(text):
	tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', '', text)
	return re.sub(r'\s', '', tmp)


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


def make_text_sig(name, title, school, phone, gmail_user, pair_version):

	#Correct 'the' case in Universities
	school = school.replace('the', 'The', 1)
	first_name = name.split(' ')[0]
	post = title.split(',')[0]
	department = title.split(',')[1]

	if pair_version == 'A':

		sig_text = inspect.cleandoc("""
			{0}

			{1}
			{2}
			{3}
			{4} | {5}
		""".format(first_name, name, title, school, phone, gmail_user))

	elif pair_version == 'B':

		sig_text = inspect.cleandoc("""

			{0}
			{1}
			{2}
			{3}
			Phone: {4}
		""".format(name, post, department, school, phone))

	return sig_text

def make_html_sig(name, title, school, phone, gmail_user, rgb, pair_version):

	#Correct 'the' case in Universities
	school = school.replace('the', 'The', 1)
	print(phone)
	#Make Phone Link
	phone_link = "+1{}".format(remove_punct(phone).strip())
	first_name = name.split(' ')[0]
	post = title.split(',')[0]
	department = title.split(',')[1]

	if pair_version == 'A':
		sig_html = """<div style="font-family:Tahoma;font-size:13px"><font face="Garamond" size="3" style="background-color:rgb(255,255,255);color:rgb(0,0,0)">{0}</font></div>
		<br>
		<div style="font-family:Tahoma;font-size:13px"><font face="Garamond" size="3" style="background-color:rgb(255,255,255);color:rgb(0,0,0)">{1}</font></div>
		<div style="font-family:Tahoma;font-size:13px"><font face="Garamond" size="3" style="background-color:rgb(255,255,255);color:rgb(0,0,0)">{2}</font></div>
		<div style="font-family:Tahoma;font-size:13px"><font face="Copperplate" size="3" style="background-color:rgb(255,255,255);color:rgb({7})">{3}</b></font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Garamond"></span><a href="tel:{5}" value="{5}" style="color:rgb(17,131,204)" target="_blank">{4}</a><span>&nbsp;</span>|<span>&nbsp;</span><a href="mailto:{6}" class="m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560m_2319474238175162055dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734dly-gmail m_-4756129822142185649gmail-m_4655728448235344902dly-gmail m_-4756129822142185649gmail-dly-gmail m_-4756129822142185649dly-gmail dly-gmail" style="color:rgb(17,131,204)" target="_blank">{6}</a></font></div></div>
		""".format(first_name, name, title, school, phone, phone_link, gmail_user, rgb)

	elif pair_version == 'B':
		sig_html = """
		<div style="background-color:rgb(255,255,255)"><font face="Helvetica" size="3">{0}</font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Helvetica" size="3">{1}</font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Helvetica" size="3">{2}</font></div>
		<div style="font-family:Tahoma;font-size:13px"><font face="Helvetica" size="3" style="background-color:rgb(255,255,255);color:rgb(0,0,0)">{3}</font></div>
		<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Helvetica" size="3">Phone:<span>&nbsp;<a href="tel:{5}" value="{5}" style="color:rgb(0,0,0)" target="_blank">{4}</a><span>&nbsp;</span></font></div></div>
		""".format(name, post, department, school, phone, phone_link)

	return sig_html


def make_text_cl(profile, 
				job_type,
				contact,
				contact_last_name,
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

	#Select Version of Cover Letter for Job Type
	method_name = "{}_{}".format(job_type, pair_version)

	my_cls = cl()
	cl_text = None
	try:
		cl_text = getattr(cl(), method_name)
	except AttributeError:
		raise NotImplementedError("Class `{}` does not implement `{}`"
			.format(cl().__class__.__name__, method_name))

	app_first_name = name.split(' ')[0]
	message_body = cl_text(contact, contact_last_name, job, office, company, 
						   internships, school, department, treatment, internship1, internship2)

	if add_sig is True:
		message_sig = make_text_sig(name, title, school, phone, gmail_user, pair_version)
		message_text = message_body+'\n\n'+message_sig
	else:
		message_text = message_body

	return message_text


def make_html_text_cl(profile, 
				job_type,
				contact,
				contact_last_name,
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

	#Make department lowercase in cl (if not MBA type)
	if job_type not in ['mba']:
		department = department.lower()
	else:
		pass

	#Make Text CL (no sig)
	message_text_body = make_text_cl(profile, 
								  job_type,
								  contact,
								  contact_last_name,
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
							 phone, gmail_user, pair_version)
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
		message_html = """<html><div style="color:rgb(0,0,0);font-family:&quot;Times New Roman&quot;,Times,serif,Times,EmojiFont,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;,NotoColorEmoji,&quot;Segoe UI Symbol&quot;,&quot;Android Emoji&quot;,EmojiSymbols;font-size:16px;font-style:normal;font-variant-ligatures:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;background-color:rgb(255,255,255);text-decoration-style:initial;text-decoration-color:initial"><font face="Helvetica">{}\n\n{}</div></html>
		""".format(textile.textile( message_text_body ), sig_html)

	return message_text, message_html

#join_experiment_profiles("experiment_test.csv")


