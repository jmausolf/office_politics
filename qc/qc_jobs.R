setwd("~/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/qc")
library(tidyverse)
library(stringr)


#protocol = '../protocols/experiment_2019-03-31-201507.csv'
protocol = '../protocols/experiment_2019-03-31-205720.csv'

#Base Protocol
base_protocol <- read_csv(protocol)

df <- base_protocol %>% 
  filter(!is.na(contact_email)) %>% 
  distinct(list_id, .keep_all=TRUE) %>% 
  distinct(contact_email, .keep_all=TRUE) %>% 
  filter(str_detect(position, 'Research') |
          str_detect(position, 'Clinical') |
          str_detect(position, 'UX') |
          str_detect(position, 'User') |
          str_detect(position, 'Construction') |
          str_detect(position, 'Home') |
          str_detect(position, 'University') |
          str_detect(position, 'Intern') |
          str_detect(position, 'Student') 
          ) %>% 
  arrange(position) %>% 
  select(list_id, company, position, job_type, office, office_state)

write_csv(df, "QC_jobs_filter.csv")
write_csv(df, "QC_jobs_filter_edit.csv")




