#!/bin/sh

##################################
###                            ###
###      Joshua G. Mausolf     ###
###   Department of Sociology  ###
###    University of Chicago   ###
###                            ###
##################################



#######################
## Main Folders
#######################

mkdir -p logs
mkdir -p protocols



#######################
## Data Science
#######################


#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=data_science
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/data_science_template_A.tex $subpath
        cp resume_templates/data_science_template_B.tex $subpath
        mv $subpath"/data_science_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/data_science_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying data_science_template_A.tex to ' $subpath
        echo 'copying data_science_template_B.tex to ' $subpath
done
echo 'renaming data_science_templates_A/B.tex to resume_templates_A/B.tex'

mkdir -p logs


#######################
## Stats
#######################

#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=stats
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/stats_template_A.tex $subpath
        cp resume_templates/stats_template_B.tex $subpath
        mv $subpath"/stats_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/stats_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying stats_template_A.tex to ' $subpath
        echo 'copying stats_template_B.tex to ' $subpath
done
echo 'renaming stats_templates_A/B.tex to resume_templates_A/B.tex'


#######################
## Quant
#######################

#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=quant
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/quant_template_A.tex $subpath
        cp resume_templates/quant_template_B.tex $subpath
        mv $subpath"/quant_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/quant_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying quant_template_A.tex to ' $subpath
        echo 'copying quant_template_B.tex to ' $subpath
done
echo 'renaming quant_templates_A/B.tex to resume_templates_A/B.tex'



#######################
## Computer Science
#######################

#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=computer_science
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/computer_science_template_A.tex $subpath
        cp resume_templates/computer_science_template_B.tex $subpath
        mv $subpath"/computer_science_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/computer_science_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying computer_science_template_A.tex to ' $subpath
        echo 'copying computer_science_template_B.tex to ' $subpath
done
echo 'renaming computer_science_templates_A/B.tex to resume_templates_A/B.tex'



#######################
## MBA
#######################


#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=mba
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/mba_template_A.tex $subpath
        cp resume_templates/mba_template_B.tex $subpath
        mv $subpath"/mba_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/mba_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying mba_template_A.tex to ' $subpath
        echo 'copying mba_template_B.tex to ' $subpath
done
echo 'renaming mba_templates_A/B.tex to resume_templates_A/B.tex'


#######################
## MBA - Analyst
#######################


#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=mba_analyst
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/mba_template_A.tex $subpath
        cp resume_templates/mba_template_B.tex $subpath
        mv $subpath"/mba_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/mba_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying mba_template_A.tex to ' $subpath
        echo 'copying mba_template_B.tex to ' $subpath
done
echo 'renaming mba_templates_A/B.tex to resume_templates_A/B.tex'



#######################
## MBA - Finance
#######################

#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=mba_finance
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp resume_templates/mba_finance_template_A.tex $subpath
        cp resume_templates/mba_finance_template_B.tex $subpath
        mv $subpath"/mba_finance_template_A.tex" $subpath"/resume_template_A.tex"
        mv $subpath"/mba_finance_template_B.tex" $subpath"/resume_template_B.tex"
        echo 'copying mba_finance_template_A.tex to ' $subpath
        echo 'copying mba_finance_template_B.tex to ' $subpath
done
echo 'renaming mba_finance_templates_A/B.tex to resume_templates_A/B.tex'
