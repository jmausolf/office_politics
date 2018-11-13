import sys
import subprocess
from search_jobs import *


def status_bar(start_val, end_val, bar_length=20, form='progress'):

    #Core Progress
    progress = float(start_val) / end_val
    arrow = '-' * int(round(progress * bar_length-1)) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    bar = arrow + spaces

    if form == 'progress':
        #Progress
        completed = int(round(progress * 100))
        out = "\rPercent: [{0}] {1: >5}%".format(bar, completed)

    elif form == 'countdown':
        #Countdown
        remainder = int(round(end_val - start_val))
        out = "\rCountdown: [{0}] {1: >5} seconds".format(bar, remainder)

    #Updater
    sys.stdout.write(out)
    sys.stdout.flush()


def countdown(seconds):

    for i in range(seconds+1):
        time.sleep(1)
        status_bar(i, seconds, form='countdown')

    sys.stdout.write('\n')
    sys.stdout.flush()


def cleanup_files(date, remove=True, subdir='output', force=False):
	n = 10
	indeed_jobs = 'indeed_jobs_*_{}*'.format(date)
	emp_key_tmp = '../employers_key_{}*'.format(date)
	err_no_rest = 'error_no_results_{}*'.format(date)
	total_error = 'total_errors_filtered_jobs_{}*'.format(date)

	rm_script = """
		rm all_filtered_jobs_*
		rm companies_*
		rm errors_filtered_jobs_*
		rm filtered_employers_*
		rm selected_filtered_jobs_*
		rm {0}
		rm {1}	
		rm {2}	
		rm {3}	
		""".format(	indeed_jobs,
					emp_key_tmp,
					err_no_rest,
					total_error
				   )

	mv_script = """
		mkdir -p {0}
		mv all_filtered_jobs_* {0}/. 2>/dev/null
		mv companies_* {0}/. 2>/dev/null
		mv errors_filtered_jobs_* {0}/. 2>/dev/null
		mv filtered_employers_* {0}/. 2>/dev/null
		mv selected_filtered_jobs_* {0}/. 2>/dev/null
		mv {1} {0}/. 2>/dev/null
		mv {2} {0}/. 2>/dev/null
		mv {3} {0}/. 2>/dev/null
		mv {4} {0}/. 2>/dev/null
		""".format(	subdir,
					indeed_jobs,
					emp_key_tmp,
					err_no_rest,
					total_error
				   )

	if force is True and remove is True:
		print("[*] removing files in {} seconds...".format(n))
		countdown(n)
		subprocess.call(rm_script, shell=True)
		print("[*] done.")

	if force is True and remove is False:
		print("[*] moving files to {} in {} seconds...".format(subdir, n))
		countdown(n)
		subprocess.call(mv_script, shell=True)
		print("[*] done.")


	if force is False:

		#Get User Input
		print("[*] cleanup script initiated...")
		rm_mv_mes = "[*] to remove files enter [1], to move files enter [2], "
		skip_mes  = "to skip cleanup enter [3]: "
		selection = input(rm_mv_mes+skip_mes)
		s = str(selection)
		if s == '1':

			print("[*] you are about to remove the following files:")
			print(rm_script)
			rm_mes = "[*] to confirm, enter [y], to deny enter [n]: "
			selection = input(rm_mes)
			s = str(selection)

			if s == 'y':
				print("[*] removing files in {} seconds...".format(n))
				countdown(n)
				subprocess.call(rm_script, shell=True)
				print("[*] done.")
				return
			else:
				print("[*] aborting file removal...")
				return

		elif s == '2':
			print("[*] you are about to move the following files:")
			print(mv_script)
			mv_mes = "[*] to confirm, enter [y], to deny enter [n]: "
			selection = input(mv_mes)
			s = str(selection)

			if s == 'y':
				print("[*] moving files to {} in {} seconds...".format(
																subdir, n))
				countdown(n)
				subprocess.call(mv_script, shell=True)
				print("[*] done.")
			else:
				print("[*] aborting file move...")
				return

		elif s == '3':
			print("[*] skipping cleanup...")
			return

		else:
			print("[*] skipping cleanup...")
			return
	




#cleanup_files()