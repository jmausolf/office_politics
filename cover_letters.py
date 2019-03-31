#Cover Letter Templates (In One Place)

import inspect

class cl(object):

	## Data Science Cover Letters

	def data_science_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am a doctoral candidate in {6} at {5}, where I specialize in studying recurrent neural networks for cloud computing. {3} has excellent careers in data science and artificial intelligence, and I am confident, together, we would be a great match.

			As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only developed enhanced RNN algorithms in Java, but I have also used Python, Spark, and SQL to apply deep neural nets and streamline ETL pipelines as a data science intern for both {4}. Collectively, my background in computer science as well as statistical and mathematical modeling gives me first-hand experience into the crux of today’s complex puzzles in data science and their applications at the frontier of artificial intelligence.

			Although I have a number of methodological strengths and my doctoral degree underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my programming and mathematical background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment))

		return message


	def data_science_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As a Ph.D. candidate in {6} at {5}, I research the application of nonparametric bound estimation for deep reinforcement learning, a type of computer vision. Given, {3}'s opportunities in machine learning and data science, I would love to contribute my talents.

			With my background in computer science, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my dissertation to develop a C++ library that optimizes deep learning. Moreover, I have applied my computational skills in Python, SQL, and Hadoop to improve ETL server efficiency and provide impactful analytics during my summer data science internships at {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to share actionable data intelligence or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in artificial intelligence, mathematics, and statistics illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message

	## Statistics Cover Letters

	def stats_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am a doctoral candidate in {6} at {5} specializing in Bayesian nonparametric inference. {3} has excellent careers in statistical learning, and I am confident, together, we would be a great match.

			As a statistician, I have both the theoretical knowledge and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only developed an enhanced Bayesian algorithm to improve efficiency in parallel computing, but I have also used Python and R to apply Bayesian and other statistical learning models as a research scientist intern at {8} and a data science intern at {9}. Collectively, my background in statistics and mathematics gives me first-hand experience into the crux of today’s complex puzzles in statistics and their applications at the frontier of both research and business intelligence.

			Although I have a number of methodological strengths and my doctoral degree underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my statistical background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment, internship1, internship2))

		return message


	def stats_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As a Ph.D. candidate in {6} at {5}, I research the application of machine learning to the estimation of marginal treatment effects, a novel method in causal inference. Given, {3}'s opportunities in applied statistics, I would love to contribute my talents.

			With my background in statistics, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my dissertation to author an R library that uses support vector machines to estimate marginal treatment effects and facilitate statistical analyses of causality. Moreover, I have applied my statistical skills in R, SQL, and Hadoop to conduct statistical modeling and simulations and deliver clear research insights during my summer internships at {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to share actionable research or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in statistics, computer science, and mathematics illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message


	## Quant Cover Letters

	def quant_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am a doctoral candidate in {6} at {5}, where I specialize in studying Bayesian nonparametric inference for statistical learning. {3} has excellent careers in statistics and mathematical finance, and I am confident, together, we would be a great match.

			As a statistician, I have both the theoretical knowledge and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only developed an enhanced Bayesian algorithm to improve efficiency in parallel computing, but I have also used Python, R, and SQL to apply Bayesian and machine learning models to simulate portfolio returns and optimize alpha as a quant intern at both {4}. Collectively, my background in statistics, computation, and mathematics gives me first-hand experience into the crux of today’s complex puzzles in statistical learning and their applications at the frontier of quantitative finance.

			Although I have a number of methodological strengths and my doctoral degree underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my statistics and mathematics background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment))

		return message


	def quant_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As a Ph.D. candidate in {6} at {5}, I research the application of high-dimensional Bayesian learning to sparse signal forecasting, a type of predictive quantitative modeling. Given, {3}'s opportunities in quantitative finance, I would love to contribute my talents.

			With my background in computational statistics, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my dissertation to develop a C++ library that optimizes high-dimensional Bayesian learning and sparse signal processing. Moreover, I have applied my computational skills in C++, Python, and SQL to develop automated quantitative trading strategies, simulate portfolio returns, and drive impactful investment analytics during my summer quantitative research internships at {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to share actionable data intelligence or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in statistics, computer science, and applied mathematics illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message

	## MS Computer Science Cover Letters

	def computer_science_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am a masters candidate in {6} at {5}, where I specialize in studying recurrent neural networks for cloud computing. {3} has excellent careers in software development, and I am confident, together, we would be a great match.

			As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only developed enhanced RNN algorithms in Java and used Python, Spark, and SQL to streamline data engineering, but I have also utilized CSS, JavaScript, and PHP in support of both frontend and backend development as a software engineering intern for {4}. In my spare time, I have applied my knowledge of cloud computing, Swift, and Objective-C to develop an iOS application for video meme sharing. Collectively, my background in computer science gives me first-hand experience into the crux of today’s complex puzzles in software engineering and their applications at the frontier of artificial intelligence and cloud computing.

			Although I have a number of methodological strengths and my masters degree underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate programming solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as {7}. I think you will agree that my programming background—combined with my outgoing charisma and penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, school, department, treatment))

		return message


	def computer_science_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As an M.S. candidate in {6} at {5}, I research the application of nonparametric bound estimation for deep reinforcement learning, a type of computer vision. Given, {3}'s opportunities in computer programming, I would love to contribute my talents.

			With my background in computer science, I exhibit both the academic theory and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have used my thesis to develop a C++ library that optimizes deep learning. Moreover, I have applied my computational skills in Python, SQL, and C++ to improve computational efficiency in high-performance computing as well as provide full-stack web development using React, Node.JS, and MongoDB during my summer software engineering internships at {4}. Beyond my internships, I have also pursued engineering passion projects in autonomous driving and iOS/Android application development. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to employ actionable engineering insights or my past initiatives as {7} to direct fundraisers and organize student activities.

			In combination, my collaborative skills and computational abilities in artificial intelligence and computer programming illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, school, department, treatment))

		return message


	## MBA Cover Letters

	def mba_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am an MBA candidate in {5} specializing in general management, particularly applications of corporate strategy, operations, marketing, and business intelligence. {3} has excellent careers in business management, and I am confident, together, we would be a great match.

			As an MBA candidate, I have both the strategic insight and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only led cross-functional efforts, identified key market opportunities, and influenced business strategy as an MBA intern at {7}, but I have also generated actionable business analytics during my experience as a business analyst at {8}. Collectively, my background in general management and statistics gives me first-hand experience into the crux of today’s complex puzzles in business and their applications at the frontier of corporate strategy and operations.

			Although I have a number of methodological strengths and my MBA underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate strategic solutions or spearheading fundraising initiatives and leading a diverse set of individuals during my tenure as {6}. I think you will agree that my management background—combined with my analytics capacity and outgoing penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, department, treatment, internship1, internship2))

		return message


	def mba_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As an MBA student in {5}, I understand management fundamentals and have applied experience in project management, team dynamics, product marketing, and business analytics. Given {3}'s opportunities in business, I would love to contribute my talents.

			With my business school background, I exhibit both the textbook business insights and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have applied my knowledge of business and economics to manage a product's lifecycle, guiding projects from strategic planning to development. Moreover, I have been able to not only generate impactful business analytics but also demonstrate the capacity to use this knowledge to develop business and product strategy during my experience at both {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to leverage actionable data intelligence or my past initiatives as {6} to direct fundraisers and organize group activities.

			In combination, my collaborative skills, management abilities, and analytics capacity illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, department, treatment))

		return message


	## MBA Analyst Cover Letters

	def mba_analyst_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am an MBA candidate in {5} specializing in general management, particularly applications of corporate strategy, operations, marketing, and business intelligence. {3} has excellent careers in business analytics, and I am confident, together, we would be a great match.

			As an MBA candidate, I have both the strategic insight and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only led cross-functional efforts, identified key market opportunities, and influenced business strategy as an MBA intern at {7}, but I have also generated actionable business analytics during my experience as a business analyst at {8}. Collectively, my background in general management and statistics gives me first-hand experience into the crux of today’s complex puzzles in business and their applications at the frontier of corporate strategy and operations.

			Although I have a number of methodological strengths and my MBA underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate strategic solutions or spearheading fundraising initiatives and leading a diverse set of individuals during my tenure as {6}. I think you will agree that my management background—combined with my analytics capacity and outgoing penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, department, treatment, internship1, internship2))

		return message


	def mba_analyst_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As an MBA student in {5}, I understand management fundamentals and have applied experience in project management, team dynamics, product marketing, and business analytics. Given {3}'s opportunities in business, I would love to contribute my talents.

			With my business school background, I exhibit both the textbook business insights and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have applied my knowledge of business and economics to manage a product's lifecycle, guiding projects from strategic planning to development. Moreover, I have been able to not only generate impactful business analytics but also demonstrate the capacity to use this knowledge to develop business and product strategy during my experience at {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to leverage actionable data intelligence or my past initiatives as {6} to direct fundraisers and organize group activities.

			In combination, my collaborative skills, management abilities, and analytics capacity illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, department, treatment))

		return message



	## MBA Finance Cover Letters

	def mba_finance_A(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		message = inspect.cleandoc("""Hi {0},

			I am writing in response to your notice for the {1} opening at your {2} office. I am an MBA candidate in {5} specializing in finance, particularly corporate finance, investments, strategy, and business intelligence. {3} has excellent careers in financial analysis, and I am confident, together, we would be a great match.

			As an MBA candidate, I have both the strategic insight and applied experience to make a difference at {3}. If you peruse my resume, you'll notice that I have not only assessed capital investment plans, modeled revenue forecasts, and optimized business expenditures as an MBA intern at {7}, but I have also generated actionable business analytics during my experience as a business analyst at {8}. Collectively, my background in finance and statistics gives me first-hand experience into the crux of today’s complex puzzles in business and their applications at the frontier of corporate finance and management.

			Although I have a number of methodological strengths and my MBA underscores my ability to tackle multifaceted problems, independence has its limits. Therefore, I also strive to work as a team player, whether it's by working with colleagues at {4} to communicate financial solutions or spearheading fundraising initiatives and leading a diverse set of individuals during my tenure as {6}. I think you will agree that my finance background—combined with my analytics capacity and outgoing penchant for team leadership—makes me a valuable recruit for the position at {3}.

			{0}, I am excited about this opportunity at {3} and eager to discuss next steps. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further.

			All the best,
			""".format(contact, job, office, company, internships, department, treatment, internship1, internship2))

		return message


	def mba_finance_B(self, contact, contact_last_name, job, office, company, internships, school, department, treatment, internship1, internship2):
		contact_full = "{} {}".format(contact, contact_last_name)
		message = inspect.cleandoc("""Dear {0}:

			I hope this email finds you well. I recently came across the {1} position at {3}'s {2} office. As an MBA student in {5}, I understand finance fundamentals and have applied experience in corporate finance, leadership, investment management, and business analytics. Given {3}'s opportunities in finance, I would love to contribute my talents.

			With my business school background, I exhibit both the textbook financial insights and pragmatic qualifications to be impactful at {3}. As evidenced in my resume, I have applied my knowledge of finance and economics to modeling corporate investment portfolios, minimizing production costs, and offering financial planning that optimizes business revenue and spending. Moreover, I have been able to not only generate impactful business analytics but I have also demonstrated the capacity to use this knowledge to develop financial and business strategy during my experience at {4}. Both within and outside the workplace, I embrace collaboration, such as my efforts at {4} to leverage actionable data intelligence or my past initiatives as {6} to direct fundraisers and organize group activities.

			In combination, my collaborative skills, financial management abilities, and analytics capacity illustrate the value I can bring to {3}, and I would be delighted to continue the conversation. To that end, I have attached my resume for review. I hope to hear from you shortly.

			Sincerely,
			""".format(contact_full, job, office, company, internships, department, treatment))

		return message
