setwd("~/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/")
library(tidyverse)
library(stringr)


df1 <- read_csv("logs/2019-03-26-015915_protocol_experiment_test_smtp_limits_results_pair_A.csv")


#SMTP Tests 2
dfA <- read_csv("logs/2019-03-27-000130_protocol_smtp_test2_experiment_2019-03-26-224927_results_pair_A.csv")


dfB <- read_csv("logs/2019-03-27-000130_protocol_smtp_test2_experiment_2019-03-26-224927_results_pair_B.csv")

df <- rbind(df1, dfA, dfB) %>% 
  select(profile, metadata) %>% 
  mutate(errors = str_detect(`metadata`, 'error')) %>% 
  mutate(sent = str_detect(`metadata`, 'metadata'))
table(df$profile, df$errors)
table(df$profile, df$sent)


df_err_alt <- df %>% 
  filter(errors == TRUE) %>% 
  filter(!str_detect(metadata, '550'))

df_sent_alt <- df %>% 
  filter(errors == FALSE) %>% 
  filter(!str_detect(metadata, 'metadata::Subject'))