####################################
## CORE LIBRARIES
####################################

##Load Libraries
library(tidyverse)
library(stargazer)
library(knitr)
library(pastecs)
library(forcats)
library(stringr)
library(lubridate)
library(scales)
library(DBI)
library(ggsci)
library(rbokeh)
library(bbplot)
library(magrittr)
library(qwraps2)
library(RColorBrewer)
library(ggthemes)

#Overwrite bbplot finalise_plot() function
source("bb_finalise_plot_academic.R")




####################################
## CORE FOLDERS
####################################

system("mkdir -p output")
system("mkdir -p output/plots")
system("mkdir -p output/tables")


####################################
## CORE UTIL FUNCTIONS
####################################

#Change Append = TRUE to Not Overwrite Files
save_stargazer <- function(output.file, ...) {
  output <- capture.output(stargazer(...))
  cat(paste(output, collapse = "\n"), "\n", file=output.file, append = FALSE)
}

wout <- function(plt_type, cid){
  outfile <- paste0("output/plots/", plt_type, "_", str_replace_all(tolower(cid), " ", "_"), ".png")
  return(outfile)
}


####################################
## CORE DATA SOURCE - All 
####################################



df <- read_csv("ANALYSIS_experiment_results_with_bounces_errors.csv")
print(df)


####################################
## CORE DATA SOURCE - ALL VALID
####################################


df <- read_csv("ANALYSIS_experiment_results_fec.csv")
print(df)





####################################
## CORE DATA SOURCE - FEC 
####################################

df <- read_csv("ANALYSIS_experiment_results_fec.csv")
print(df)












