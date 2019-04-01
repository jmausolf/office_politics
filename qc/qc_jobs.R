setwd("~/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/")
library(tidyverse)
library(stringr)



base_protocol <- read_csv('protocols/experiment_2019-03-31-133039.csv') 

df <- base_protocol %>% 
  filter(!is.na(contact_email)) %>% 
  distinct(list_id, .keep_all=TRUE) %>% 
  filter(str_detect(position, 'Research') |
          str_detect(position, 'Clinical') |
          str_detect(position, 'UX') |
          str_detect(position, 'User') |
          str_detect(position, 'Construction') |
          str_detect(position, 'Home')
          ) %>% 
  arrange(position) %>% 
  select(list_id, company, position, job_type, office, office_state)

write_csv(df, "QC_jobs_filter.csv")




