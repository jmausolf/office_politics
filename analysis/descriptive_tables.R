####################################
## Load SOURCE
####################################

source("analysis_source.R")

####################################
## Make Descriptive Stats Tables
####################################


# define the markup language we are working in.
options(qwraps2_markup = "latex") 


#TODO
#Could make a map of callbacks by office location, faceted by party



#Method for Total Applicants
total_applicants <- 
  list(
    "Total Job Applicants" =
      list("Applicants Sent" = ~ n_distinct(.data$index_wave),
           "Applicant Pairs Sent" = ~ n_distinct(.data$pair_index))
  )


total_applicant_stats <- 
  list(
    "Total Job Applicants" =
      list("Sent Applicants" = ~ n_distinct(.data$index_wave),
           "Received Applicants" = ~ n_perc(.data$app_sent == "1"),
           "Failed Applicants" = ~ n_perc(.data$app_sent == "0"))
  )

sent_stats_apps <- 
  list(
    "Sent Applicant Results" =
      list("Received Applicants" = ~ n_perc(.data$app_sent == "1"),
           "Failed Applicants" = ~ n_perc(.data$app_sent == "0"))
  )

sent_stats_pairs <- 
  list(
    "Sent Applicant Pair Results" =
      list("Received Applicant Pairs" = ~ n_perc(.data$pair_sent == "1"),
           "Failed Applicant Pairs" = ~ n_perc(.data$pair_sent == "0"))
  )



#Method for Profiles
total_profiles <-
  list(
    "Applicant Profiles" =
      list("P01DH" = ~ n_perc(.data$profile_P01DH),
           "P02DL" = ~ n_perc(.data$profile_P02DL),
           "P03NH" = ~ n_perc(.data$profile_P03NH),
           "P04NL" = ~ n_perc(.data$profile_P04NL),
           "P05RH" = ~ n_perc(.data$profile_P05RH),
           "P06RL" = ~ n_perc(.data$profile_P06RL)
      ),
      
      "Applicant Partisanship" =
      list("Republican" = ~ n_perc(.data$party_REP),
           "Neutral" = ~ n_perc(.data$party_NEU),
           "Democrat" = ~ n_perc(.data$party_DEM)
      ),
    
      "Applicant Prestige" =
      list("High Prestige" = ~ n_perc(.data$prestige_H),
           "Lower Prestige" = ~ n_perc(.data$prestige_L)
      )

  )



#Method for Job Types, Locations
total_jobs <-
  list(
    "Job Type" =
      list("Data Science" = ~ n_perc(.data$job_type_data_science),
           "Quantitative Finance" = ~ n_perc(.data$job_type_quant),
           "Statistics" = ~ n_perc(.data$job_type_stats),
           "Computer Science" = ~ n_perc(.data$job_type_computer_science),
           "MBA - Analyst" = ~ n_perc(.data$job_type_mba_analyst),
           "MBA - Finance" = ~ n_perc(.data$job_type_mba_finance),
           "MBA - Project Management" = ~ n_perc(.data$job_type_mba)
      ),
    
    "Job Region" =
      list("Northeast" = ~ n_perc(.data$region_northeast),
           "Mid-Atlantic" = ~ n_perc(.data$region_midatlantic),
           "Midwest" = ~ n_perc(.data$region_midwest),
           "South" = ~ n_perc(.data$region_south),
           "West" = ~ n_perc(.data$region_westcoast)
      )
    
  )



#Method for Results
result_stats_apps <- 
  list(
    "Application Results" =
      list("Received Callback" = ~ n_perc(.data$callback_binary),
           "Recieved Other Reply" = ~ n_perc(.data$reply_only),
           "Recieved Any Response" = ~ n_perc(.data$response_binary))
  )






#########################################
## All Applicants (Received and Failed)
#########################################

df <- dfb


#Make Applicants Data
applicants <- df %>% 
  summary_table(total_applicants)


#Make Waves, Successfully Sent, Failed
sent_stats <- df %>% 
  select(index_wave, pair_index, bounce_error_other_binary, pair_beo_bin) %>% 
  mutate(app_sent = if_else(bounce_error_other_binary != 1, 1, 0)) %>% 
  mutate(pair_sent = if_else(pair_beo_bin == 0, 1, 0))

#Applicant All Stats
applicant_stats <- sent_stats %>% 
  summary_table(total_applicant_stats)


#Applicants Stats
ssa <- sent_stats %>% 
  summary_table(sent_stats_apps) 

#Pair Stats
ssp <- sent_stats %>% 
  distinct(pair_index, .keep_all = TRUE)  %>% 
  summary_table(sent_stats_pairs) 
colnames(ssp) <- ". (N = 3,856)"
colnames(ssp)



#Make Applicants Profiles
df_stats <- dummy_cols(df, select_columns = c("profile", 
                                              "prestige",
                                              "party",
                                              "region",
                                              "job_type"))
profiles <- df_stats %>% 
  summary_table(total_profiles) 

jobs <- df_stats %>% 
  summary_table(total_jobs) 



#Callback Stats
cb_stats <- df %>% 
  select(index_wave, callback_binary, reply_binary, response_binary) %>% 
  mutate(reply_only = if_else( (reply_binary == 1 & callback_binary !=1), 1, 0)) %>% 
  summary_table(result_stats_apps) 




#Combined Table for All Data
#tab_all <- rbind(applicants, ssa, ssp, profiles, cb_stats) 
tab_all <- rbind(applicant_stats, cb_stats, profiles, jobs)
tab_all





#########################################
## Received Applicants Only
#########################################


df <- dfa


#Make Waves, Successfully Sent, Failed
sent_stats <- df %>% 
  select(index_wave, pair_index, bounce_error_other_binary, pair_beo_bin) %>% 
  mutate(app_sent = if_else(bounce_error_other_binary != 1, 1, 0)) %>% 
  mutate(pair_sent = if_else(pair_beo_bin == 0, 1, 0))

#Applicant All Stats
applicant_stats <- sent_stats %>% 
  summary_table(total_applicant_stats)



#Make Applicants Profiles
df_stats <- dummy_cols(df, select_columns = c("profile", 
                                              "prestige",
                                              "party",
                                              "region",
                                              "job_type"))
profiles <- df_stats %>% 
  summary_table(total_profiles) 

jobs <- df_stats %>% 
  summary_table(total_jobs) 



#Callback Stats
cb_stats <- df %>% 
  select(index_wave, callback_binary, reply_binary, response_binary) %>% 
  mutate(reply_only = if_else( (reply_binary == 1 & callback_binary !=1), 1, 0)) %>% 
  summary_table(result_stats_apps) 




#Combined Table for All Data
#tab_all <- rbind(applicants, ssa, ssp, profiles, cb_stats) 
tab_received <- rbind(applicant_stats, cb_stats, profiles, jobs)
tab_received






#########################################
## FEC Matched, Received Applicants Only
#########################################


df <- dfec


#Make Applicants Data
applicants <- df %>% 
  summary_table(total_applicants)


#Make Waves, Successfully Sent, Failed
sent_stats <- df %>% 
  select(index_wave, pair_index, bounce_error_other_binary, pair_beo_bin) %>% 
  mutate(app_sent = if_else(bounce_error_other_binary != 1, 1, 0)) %>% 
  mutate(pair_sent = if_else(pair_beo_bin == 0, 1, 0))

#Applicant All Stats
applicant_stats <- sent_stats %>% 
  summary_table(total_applicant_stats)


#Make Applicants Profiles
df_stats <- dummy_cols(df, select_columns = c("profile", 
                                              "prestige",
                                              "party",
                                              "region",
                                              "job_type"))
profiles <- df_stats %>% 
  summary_table(total_profiles) 

jobs <- df_stats %>% 
  summary_table(total_jobs) 



#Callback Stats
cb_stats <- df %>% 
  select(index_wave, callback_binary, reply_binary, response_binary) %>% 
  mutate(reply_only = if_else( (reply_binary == 1 & callback_binary !=1), 1, 0)) %>% 
  summary_table(result_stats_apps) 




#Combined Table for All Data
#tab_all <- rbind(applicants, ssa, ssp, profiles, cb_stats) 
tab_fec <- rbind(applicant_stats, cb_stats, profiles, jobs)
tab_fec





#########################################
## Make Final Table
#########################################


final_table <- cbind(tab_all, tab_received, tab_fec)
final_table



capture.output(print(final_table,
                     booktabs = TRUE,
                     rtitle = "Summary Statistics",
                     cnames = c("Sent Applicants", "Received Applicants", "FEC Matched Applicants")), 
               file="output/tables/table_descriptive_stats_test.tex")
