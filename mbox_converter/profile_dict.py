profiles_dict = {

'P01DH': 'grahamsrandersen@gmail.com',
'P02DL': 'briandnlarsen@gmail.com',
'P03NH': 'ryancrmcgrath@gmail.com',
'P04NL': 'dustinrtstein@gmail.com',
'P05RH': ['matthewzrhartman@gmail.com', 'matthewzchartman@gmail.com'],
'P06RL': 'codyhtwalsh@gmail.com'
}


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