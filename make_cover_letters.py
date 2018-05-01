import random
import pandas as pd
from new_messages import *
import textwrap
import inspect
import textile
from internship_key import internship_keys


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
	sig_text = inspect.cleandoc("""

		{0}
		{1}
		{2}
		C: {3} | {4}
	""".format(name, title, school, phone, gmail_user))

	return sig_text

def make_html_sig(name, title, school, phone, gmail_user):

	phone_link = "+1{}".format(phone.replace('-', ''))

	sig_html = """
	<div style="background-color:rgb(255,255,255)"><font face="Copperplate" size="3">{0}</font>
	</div>
	<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Copperplate">{1}</font>
	</div>
	<div style="font-family:Tahoma;font-size:13px"><font face="Copperplate" color="#800000" size="3" style="background-color:rgb(255,255,255)">{2}</font></div>
	<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Copperplate">C:<span>&nbsp;</span><a href="tel:{3}" value="{4}" style="color:rgb(17,85,204)" target="_blank">336-948-0756</a><span>&nbsp;</span>|<span>&nbsp;</span><a href="mailto:{5}" class="m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560m_2319474238175162055dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734dly-gmail m_-4756129822142185649gmail-m_4655728448235344902dly-gmail m_-4756129822142185649gmail-dly-gmail m_-4756129822142185649dly-gmail dly-gmail" style="color:rgb(17,85,204)" target="_blank">{5}</a></font></div></div>
	""".format(name, title, school, phone, phone_link, gmail_user)

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
				treatment,
				phone, 
				gmail_user,
				add_sig=True
				):


	ik = "{}_{}".format(job_type, profile[-1])
	intern_key = internship_keys[ik]
	internships = sub_cover_letter_internship(company, intern_key)


	#method_name = "{}_{}".format(profile, job_type)
	method_name = "{}".format(job_type)
	my_cls = cl()

	cl_text = None
	try:
		cl_text = getattr(cl(), method_name)
	except AttributeError:
		raise NotImplementedError("Class `{}` does not implement `{}`"
			.format(cl().__class__.__name__, method_name))

	message_body = cl_text(contact, job, office, company, internships, school, department, treatment)

	if add_sig is True:
		message_sig = make_text_sig(name, title, school, phone, gmail_user)
		message_text = message_body+'\n\n'+message_sig
		#print(message_text)
	else:
		message_text = message_body

	#print(message_text)
	return message_text, internships





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
				treatment,
				phone, 
				gmail_user
				):

	#Make Text CL (no sig)
	message_output = make_text_cl(profile, job_type, contact, job, office, company, name, title, school, department, treatment, phone, gmail_user, add_sig=False)
	message_text_body = message_output[0]
	internships = message_output[1]

	#Make Text Sig/Full Text Message
	sig_text = make_text_sig(name, title, school, phone, gmail_user)
	message_text = message_text_body+'\n\n'+sig_text
	#print(message_text)

	#Make HTML Sig
	sig_html = make_html_sig(name, title, school, phone, gmail_user)

	#Make HTML Message from Text CL and HTML Sig
	#(needed to keep the internships consistent)
	message_html = """<html><div style="color:rgb(0,0,0);font-family:&quot;Times New Roman&quot;,Times,serif,Times,EmojiFont,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;,NotoColorEmoji,&quot;Segoe UI Symbol&quot;,&quot;Android Emoji&quot;,EmojiSymbols;font-size:16px;font-style:normal;font-variant-ligatures:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;background-color:rgb(255,255,255);text-decoration-style:initial;text-decoration-color:initial">{}\n\n{}</div></html>
	""".format(textile.textile( message_text_body ), sig_html)
	#print(message_html)

	return message_text, message_html, internships




"""
def join_profiles_credentials():
	cred = pd.read_csv("credentials.csv")
	prof = pd.read_csv("profiles.csv")

	df = pd.merge(cred, prof, on=['profile'])
	return df

def join_experiment_profiles(experiment_file):
	experiment = pd.read_csv(experiment_file)
	profiles = join_profiles_credentials()
	df = pd.merge(experiment, profiles, on=['profile'])

	#df['intern_key'] = internship_keys['data_science_H']
	print(df)
	return df
"""



#join_experiment_profiles("experiment_test.csv")

