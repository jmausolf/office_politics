####################################
## CORE LIBRARIES
####################################


setwd("~/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/analysis/")


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
library(fastDummies)

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



dfb <- read_csv("ANALYSIS_experiment_results_with_bounces_errors.csv")
print(df)


####################################
## CORE DATA SOURCE - ALL VALID
####################################


dfa <- read_csv("ANALYSIS_experiment_results.csv")
print(df)





####################################
## CORE DATA SOURCE - FEC 
####################################




dfec <- read_csv("ANALYSIS_experiment_results_fec.csv")


dfec <- dfec %>% 
  # select(index_wave, company, cid_master, cluster_party,
  # 		mean_pid2, median_pid2, mean_ps, median_ps, pid2_percent_rank,
  # 		polarization_raw_pid_percent_rank,
  # 		partisan_score_percent_rank, polarization_raw_ps_percent_rank,
  # 		party, callback_binary, pair_callback_bin) %>%
  
  #make various party vars
  
  #party1
  mutate(party0 = cluster_party) %>% 
  mutate(party1 = if_else(mean_pid2 <= 1.50, "DEM", "REP")) %>% 
  mutate(party2 = if_else(median_pid2 <= 1.50, "DEM", "REP")) %>%
  mutate(party3 = if_else(mean_ps <= 0.00, "DEM", "REP")) %>% 
  mutate(party4 = if_else(median_ps <= 0.00, "DEM", "REP")) %>% 
  mutate(party5 = if_else(pid2_percent_rank < 0.500, "DEM", "REP")) %>%
  mutate(party6 = if_else(partisan_score_percent_rank < 0.500, "DEM", "REP")) %>%

  #make partisan dummy
  mutate(partisan = if_else(party != "NEU", 1, 0))  %>% 



  #make party match variables
  #filter(callback_binary >= 1) %>% 


  #make party match variables
  mutate(pm0 = 
           ifelse((party == party0 & party != "NEU"), 1,
                  ifelse((party != party0 & party != "NEU"), -1, 0))) %>% 
  mutate(pm1 = 
           ifelse((party == party1 & party != "NEU"), 1,
                  ifelse((party != party1 & party != "NEU"), -1, 0))) %>% 
  mutate(pm2 = 
           ifelse((party == party2 & party != "NEU"), 1,
                  ifelse((party != party2 & party != "NEU"), -1, 0))) %>% 
  mutate(pm3 = 
           ifelse((party == party3 & party != "NEU"), 1,
                  ifelse((party != party3 & party != "NEU"), -1, 0))) %>%   
  mutate(pm4 = 
           ifelse((party == party4 & party != "NEU"), 1,
                  ifelse((party != party4 & party != "NEU"), -1, 0))) %>%         
  mutate(pm5 = 
           ifelse((party == party5 & party != "NEU"), 1,
                  ifelse((party != party5 & party != "NEU"), -1, 0))) %>%          
  mutate(pm6 = 
           ifelse((party == party6 & party != "NEU"), 1,
                  ifelse((party != party6 & party != "NEU"), -1, 0))) %>%

  #make factors
  mutate(pm0f = ordered(pm0, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm1f = ordered(pm1, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm2f = ordered(pm2, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm3f = ordered(pm3, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm4f = ordered(pm4, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm5f = ordered(pm5, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match"))) %>%
  mutate(pm6f = ordered(pm6, levels = c(-1, 0, 1), 
         labels=c("mismatch", "neutral", "match")))




dfc <- dfec %>% 
  select(callback_binary, pm0, pm1, pm2, pm3, pm4, pm5, pm6, pair_callback_bin) %>%
  filter(pair_callback_bin >= 1) %>% 
  select(callback_binary, pm0, pm1, pm2, pm3, pm4, pm5, pm6)


cor(dfc, method = c("spearman"))


table(dfc$callback_binary, dfc$pm0)
table(dfc$callback_binary, dfc$pm1)
table(dfc$callback_binary, dfc$pm2)
table(dfc$callback_binary, dfc$pm3)
table(dfc$callback_binary, dfc$pm4)
table(dfc$callback_binary, dfc$pm5)
table(dfc$callback_binary, dfc$pm6)


#number 1 or 2 seem best




