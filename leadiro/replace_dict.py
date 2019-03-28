


#IDEA to Make a Dict Replacement Key for the Employers Key 
#Such that the employers in that key are fixed so that they align in the fuzzy match?


emp_key_adjustments = {
	'J.Crew Group':'J. Crew Group',
	'ICF':'ICF International'
	
}



#need to do something with faulty matches from leadiro from abm
#e.g. speedway llc downloaded, but needed International Speedway Corp
#Simply create a blacklist such that if the company == X on the 
#combined CSV, drop the row

#drop
#Speedway LLC

leadiro_changes = {
	'Visa Inc. (Visa)':'Visa',
	'Davita Inc.':'Davita',
	'Cross Country Healthcare, Inc. (Cross Country)':'Cross Country Healthcare'
}


blacklist_companies = {
	'Speedway LLC':None
}

