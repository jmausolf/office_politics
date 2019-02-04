#!/bin/sh

##################################
###                            ###
###      Joshua G. Mausolf     ###
###   Department of Sociology  ###
###    University of Chicago   ###
###                            ###
##################################


#TODO 
#Unique Resume Types for Jobs
#Data Science, Stats, Quant are Roughly the Same Type
#Managerment Consulting and Law Different?


#Copy Same Resume Template to Each Folder
#for profile in P0{1DH,2DL,3NH,4NL,5RH,6RL}; do
#    for topic in {data_science,management_consulting,quant}; do
#        mkdir -p "$profile/$topic/tex"
#        cp resume_template.tex "$profile/$topic/tex"
#        #cp Resume_Matthew_Zachary_Hartman.pdf "$profile/$topic" 
#    done
#done


#Copy Same Resume to Each Partisan Folder
#for profile in P0{1DH,2DL,5RH,6RL}; do
#  for topic in {data_science,stats,quant,mba,consultant,law}; do
#        mkdir -p "$profile/$topic/tex"
#        subpath="$profile/$topic/tex"
#        cp resume_templates/partisan_resume_template.tex $subpath
#        mv $subpath/partisan_resume_template.tex $subpath/resume_template.tex
#        echo 'copying partisan_resume_template.tex to ' $subpath
#    done
#done


#Copy Neutral Resume to Each Neutral Folder
#for profile in P0{3NH,4NL}; do
#  for topic in {data_science,stats,quant,mba,consultant,law}; do
#        mkdir -p "$profile/$topic/tex"
#        subpath="$profile/$topic/tex"
#        cp resume_templates/neutral_resume_template.tex $subpath
#        mv $subpath/neutral_resume_template.tex $subpath/resume_template.tex
#        echo 'copying neutral_resume_template.tex to ' $subpath
#    done
#done

#######################
## Basic Template All 
#######################


#Copy A and B Versions of Resume to Each Folder
#for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
#  for topic in {data_science,stats,quant,mba,consultant,law}; do
#        mkdir -p "$profile/$topic/tex"
#        subpath="$profile/$topic/tex"
#        cp resume_templates/resume_template_A.tex $subpath
#        cp resume_templates/resume_template_B.tex $subpath
#        echo 'copying resume_template_A.tex to ' $subpath
#        echo 'copying resume_template_B.tex to ' $subpath
#    done
#done

#mkdir -p logs



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

mkdir -p logs


#######################
## Quant
#######################



#######################
## Computer Science
#######################







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

mkdir -p logs


#######################
## Consultant
#######################


#Copy A and B Versions of Resume to Each Folder
for profile in P0{1DH,2DL,5RH,6RL,3NH,4NL}; do
  topic=consultant
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

mkdir -p logs



