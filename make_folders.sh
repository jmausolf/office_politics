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
for profile in P0{1DH,2DL,5RH,6RL}; do
  for topic in {data_science,stats,quant,mba,consultant,law}; do
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp partisan_resume_template.tex $subpath
        mv $subpath/partisan_resume_template.tex $subpath/resume_template.tex
        echo 'copying partisan_resume_template.tex to ' $subpath
    done
done


#Copy Neutral Resume to Each Neutral Folder
for profile in P0{3NH,4NL}; do
  for topic in {data_science,stats,quant,mba,consultant,law}; do
        mkdir -p "$profile/$topic/tex"
        subpath="$profile/$topic/tex"
        cp neutral_resume_template.tex $subpath
        mv $subpath/neutral_resume_template.tex $subpath/resume_template.tex
        echo 'copying neutral_resume_template.tex to ' $subpath
    done
done

mkdir -p logs

