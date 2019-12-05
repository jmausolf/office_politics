####################################
## Load SOURCE
####################################

#source("indiv_source.R")
#source("indiv_vartab_varplot_functions.R")



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



#Method for Sent Applicant Stats (Received/Failed)
# sent_stats <- 
#   list(
#     "Received Applications" =
#       list("Received Applicants" = ~ n_perc(sent_stats_all$app_sent == "1"),
#            "Received Applicant Pairs" = ~ n_perc(sent_stats_all$pair_sent == "1")),
#     
#     "Failed Applications" =
#       list("Failed Applicants" = ~ n_perc(sent_stats_all$app_sent == "0"),
#            "Failed Applicant Pairs" = ~ n_perc(sent_stats_all$pair_sent == "0"))
#   )


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



#Method for Total Contrib
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



#Method for Results
result_stats_apps <- 
  list(
    "Application Results" =
      list("Received Callback" = ~ n_perc(.data$callback_binary),
           "Recieved Other Reply" = ~ n_perc(.data$reply_only),
           "Recieved Any Response" = ~ n_perc(.data$response_binary))
  )






################################
## Main Table / All Periods
################################

df <- dfb


#Make Applicants Data
applicants_all <- df %>% 
  summary_table(total_applicants)


#Make Waves, Successfully Sent, Failed
sent_stats_all <- df %>% 
  select(index_wave, pair_index, bounce_error_other_binary, pair_beo_bin) %>% 
  mutate(app_sent = if_else(bounce_error_other_binary != 1, 1, 0)) %>% 
  mutate(pair_sent = if_else(pair_beo_bin == 0, 1, 0))

#Applicants Stats
ssa <- sent_stats_all %>% 
  summary_table(sent_stats_apps) 

#Pair Stats
ssp <- sent_stats_all %>% 
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
profiles_all <- df_stats %>% 
  summary_table(total_profiles) 



#Callback Stats
cb_stats_all <- df %>% 
  select(index_wave, callback_binary, reply_binary, response_binary) %>% 
  mutate(reply_only = if_else( (reply_binary == 1 & callback_binary !=1), 1, 0)) %>% 
  summary_table(result_stats_apps) 




#Combined Table for All Data
tab_all <- rbind(applicants_all, ssa, ssp, profiles_all, cb_stats_all) 
tab_all


capture.output(print(tab_all,
                     rtitle = "Summary Statistics",
                     cnames = c("All Applicants")), 
               file="output/tables/table_descriptive_stats_test.tex")

