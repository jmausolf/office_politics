profiles_dict = {

'P01DH': 'grahamsrandersen@gmail.com',
'P02DL': 'briandnlarsen@gmail.com',
'P03NH': 'ryancrmcgrath@gmail.com',
'P04NL': 'dustinrtstein@gmail.com',
'P05RH': ['matthewzrhartman@gmail.com', 'matthewzchartman@gmail.com'],
'P06RL': 'codyhtwalsh@gmail.com'
}


mbox_dict = {

'P01DH_W1': 'grahamsrandersen@gmail.com',
'P01DH_W2': 'grahamsrandersen@gmail.com',
'P02DL_W1': 'briandnlarsen@gmail.com',
'P02DL_W2': 'briandnlarsen@gmail.com',
'P03NH_W1': 'ryancrmcgrath@gmail.com',
'P03NH_W2': 'ryancrmcgrath@gmail.com',
'P04NL_W1': 'dustinrtstein@gmail.com',
'P04NL_W2': 'dustinrtstein@gmail.com',
'P05RH_W1A': 'matthewzchartman@gmail.com',
'P05RH_W2': 'matthewzchartman@gmail.com',
'P05RH_W1B': 'matthewzrhartman@gmail.com',
'P06RL_W1': 'codyhtwalsh@gmail.com',
'P06RL_W2': 'codyhtwalsh@gmail.com'
}


def profile_sender(email_address, profiles_list):
	if email_address in profiles_list:
		return True
	else:
		return False

def mbox_email(mbox_key):
	print(mbox_dict[mbox_key])
	return mbox_dict[mbox_key]

def ret_mbox_email(mbox_name):
	mbox_key = mbox_name.split('-')[0]
	mbox_key = mbox_key.split('.mbox')[0]
	to_email = mbox_email(mbox_key)
	return to_email


profile_emails = []
for k, v in profiles_dict.items():
	if isinstance(v, (str)):
		profile_emails.append(v)
	elif isinstance(v, (list)):
		[profile_emails.append(e) for e in v]

	else:
		pass
print('[*] loading the following profile email addresses...')
print(profile_emails)

#tests = ["jgm346@gmail.com", 'grahamsrandersen@gmail.com', 'matthewzchartman@gmail.com', 'jmausolf@uchicago.edu']
#tr = [profile_sender(t, profile_emails) for t in tests]
#print(tr)