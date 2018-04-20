#!/bin/sh

##################################
###                            ###
###      Joshua G. Mausolf     ###
###   Department of Sociology  ###
###    University of Chicago   ###
###                            ###
##################################


#profiles='P01DH P02DL P03NH P04NL P05RH P06RL'

#topics=datascience managementconsulting quant chemicalengineer

#profiles=('P01DH' 'P02DL' 'P03NH' 'P04NL' 'P05RH' 'P06RL')

#mkdir -p {P01DH,P02DL,P03NH,P04NL,P05RH,P06RL}/{folder1,folder2,folder3,folder4,folder5,folder6,folder7,folder8}


#mkdir -p {P01DH,P02DL,P03NH,P04NL,P05RH,P06RL}/{data_science,management_consulting,quant}

for profile in P0{1DH,2DL,3NH,4NL,5RH,6RL}; do
    for topic in {data_science,management_consulting,quant}; do
        mkdir -p "$profile/$topic"
        cp messages.py "$profile/$topic"
        cp Resume_Matthew_Zachary_Hartman.pdf "$profile/$topic"
    done
done





# set counter value to 0
#c=0
# loop trough the array l1 (while the counter $c is less than the length of the array $l1)
#while [ "$c" -lt "${#profiles[@]}" ]; do
  # echo the corresponding value of array l2 to the file.txt in the directory
  #echo "${topics[$c]}"
  #echo "${profiles[$c]}${topics[$c]}"
  # increment the counter
  #let c=c+1
#done