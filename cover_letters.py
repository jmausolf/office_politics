#Cover Letter Templates (In One Place)
#from make_cover_letters import *

import inspect

class cl(object):

	## Data Science Cover Letters 

	def data_science_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment):
		message = inspect.cleandoc("""Dear {0},

			I am writing in response to your notice for the {1} position at your {2} office. I am a doctoral candidate in {6} at {5}, specializing in the application of recurrent neural networks in cloud computing. {3} is a leader in data science and artificial intelligence, and I am confident, together, we would be a great match.

			As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at {3}. As you can see from my resume, I have not only developed enhanced RNN algorithms in Java, but also used Python, Scala, and SQL to apply deep neural nets and streamline ETL pipelines as a data science intern for both {4}. Collectively, my background in computer science, statistics, and mathematical modeling gives me first-hand experience into the crux of today’s complex puzzles in data science and their applications at the frontier of artificial intelligence.

			Although I have strong methodological strengths and my doctoral degree underscores my ability to tackle complex problems, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my programming background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the data scientist position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment))

		return message


	def data_science_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As a Ph.D. candidate in {6} at {5}, I research the application of nonparametric bound estimation for deep reinforcement learning, a type of computer vision. Given, {3}'s opportunities in machine learning and data science, I would love to contribute my talents.

			With my background in computer science, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my dissertation to develop a C++ library that optimizes deep learning. Moreover, I have applied my computational skills in Python, SQL, and Hadoop to improve ETL server efficiency and provide impactful analytics as a summer data science intern for both {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to share actionable data solutions or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in artificial intelligence, mathematics, and statistics, illustrate the value I could bring to {3}, and I am delighted to submit my application. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message

	## Statistics Cover Letters


	## MBA Cover Letters 

	def mba_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment):
		message = inspect.cleandoc("""Dear {0},

			I am writing in response to your notice for the {1} position at your {2} office. I am an MBA candidate in the {6} at {5}, specializing in the application of recurrent neural networks in cloud computing. {3} is a leader in data science and artificial intelligence, and I am confident, together, we would be a great match.

			As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at {3}. As you can see from my resume, I have not only developed enhanced RNN algorithms in Java, but also used Python, Scala, and SQL to apply deep neural nets and streamline ETL pipelines as a data science intern for both {4}. Collectively, my background in computer science, statistics, and mathematical modeling gives me first-hand experience into the crux of today’s complex puzzles in data science and their applications at the frontier of artificial intelligence.

			Although I have strong methodological strengths and my doctoral degree underscores my ability to tackle complex problems, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my programming background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the data scientist position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment))

		return message


	def mba_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As an MBA student in the {6} at {5}, I research the application of nonparametric bound estimation for deep reinforcement learning, a type of computer vision. Given, {3}'s opportunities in machine learning and data science, I would love to contribute my talents.

			With my background in computer science, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my dissertation to develop a C++ library that optimizes deep learning. Moreover, I have applied my computational skills in Python, SQL, and Hadoop to improve ETL server efficiency and provide impactful analytics as a summer data science intern for both {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to share actionable data solutions or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in artificial intelligence, mathematics, and statistics, illustrate the value I could bring to {3}, and I am delighted to submit my application. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message










