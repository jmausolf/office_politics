#Cover Letter Templates (In One Place)
#from make_cover_letters import *

import inspect

class cl(object):


	def P05RH_data_science(self, contact, job, office, company, internships):
		message = inspect.cleandoc("""Dear {0}:

			I am writing in response to your notice for the {1} position at your {2} office. I am a doctoral candidate in Computer Science at Stanford University, specializing in the application of recurrent neural networks in cloud computing. {3} is a leader in data science and artificial intelligence, and I am confident, together, we would be a great match.

			As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at {3}. As you can see from my resume, I have not only developed enhanced RNN algorithms in Java, but also used Python, Scala, and SQL to apply deep neural nets and streamline ETL pipelines as a data science intern for both {4}. Collectively, my background in computer science, statistics, and mathematical modeling gives me first hand experience into the crux of today’s complex computational puzzles in data science and their applications at the frontiers of artificial intelligence.

			Although I have strong methodological strengths and my doctoral degree underscores my ability to tackle complex problems, I also strive to work as a team player, whether its by collaborating with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as president of the Harvard Republican Club. I think you will agree that my computational background—combined with my outgoing charisma and penchant for collaborative leadership—makes me a valuable recruit for the data scientist position at {3}.

			I want you to know that I am excited to submit my application to {3}. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			Warm regards,
			""".format(contact, job, office, company, internships))

		#print(message)
		return message












#private-elite vs. private non-elite
treatments = {
	'P01DH' : 'Harvard College Democrats',
	'P02DL' : 'Elmira College Democrats',
	'P03NH' : 'Yale College Council',
	'P04NL' : 'Hartwick Student Senate',
	'P05RH' : 'Princeton College Republicans',
	'P06RL' : 'Houghton College Republicans'
}

#Graduate Programs?




