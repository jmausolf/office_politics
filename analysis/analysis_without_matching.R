######################################
## Load Libraries & Data
######################################


library(Rmisc)
library(Hmisc)
library(tidyverse)


df <- read_csv("ANALYSIS_experiment_results.csv")
#df <- read_csv("ANALYSIS_experiment_results_with_bounces_errors.csv")
print(df)
df_test <- df %>% 
  select(callback_binary, profile, company, pair_callback_bin) %>% 
  filter(callback_binary == 1) %>% 
  distinct()
#   filter(matched_pair == "A")




table(df$profile, df$callback_binary)


df2 <- df %>% 
  #filter(pair_callback_bin != 2) %>% 
  select(profile, callback_binary, prestige, party) %>% 
  group_by(profile) %>% 
  add_tally(callback_binary, name = "total_callbacks") %>% 
  add_count(profile, name = "total_applications") %>% 
  mutate(proportion_callback = total_callbacks / total_applications) %>% 
  #mutate(uci_cb = binconf(total_callbacks, total_applications, alpha=0.05)) %>% 
  select(-callback_binary) %>% 
  #sort(profile) %>% 
  distinct()





table(df2$profile, df2$callback_binary)

binconf(df2$total_callbacks, df2$total_applications, alpha=0.1, method=c("asymptotic"))


binconf(df2$total_callbacks, df2$total_applications, alpha=0.05, method=c("asymptotic"))




df3 <- df %>% 
  select(profile, callback_binary) %>% 
  group_by(profile) %>% 
  add_tally(callback_binary, name = "total_callbacks") %>% 
  add_count(profile, name = "total_applications") %>% 
  mutate(proportion_callback = total_callbacks / total_applications) %>% 
  mutate(p = proportion_callback,
         n = total_applications) %>% 
  mutate(prop_cb_se = sqrt(p*(1-p)/n)) %>% 
  
  select(-callback_binary) %>% 
  distinct()



df4 <- df %>% 
  filter(pair_callback_bin == 1) %>% 
  select(profile, callback_binary) %>% 
  group_by(profile) %>% 
  summarize(mean_cb = mean(callback_binary), 
            uci_cb = CI(callback_binary)[1], 
            lci_cb = CI(callback_binary)[3])

#Try to look at graphical analysis of other audit studies
#bar graph total, percentages, 
#total callback would make sense if equal groups sent
#with unequal groups, need percents/proportions 


#Should also look at matched pair analyses vs. single pair
#twice as many neutral apps...

## Graph Percentages


ggplot(df2, aes(party, proportion_callback)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  facet_grid(~prestige) +
  scale_y_continuous(labels = scales::percent) 



ggplot(df2, aes(prestige, proportion_callback)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  facet_grid(~party) +
  scale_y_continuous(labels = scales::percent) 




## Graph Total Callbacks
ggplot(df2, aes(profile, total_callbacks)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") 



ggplot(df2, aes(party, total_callbacks)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  facet_grid(~prestige) 



df4 <- df %>% 
  #filter(pair_callback_bin != 2) %>% 
  select(profile, callback_binary) %>% 
  group_by(profile) %>% 
  summarize(mean_cb = mean(callback_binary), 
            uci_cb = CI(callback_binary)[1], 
            lci_cb = CI(callback_binary)[3])


## Graph Percentages
ggplot(df4, aes(profile, mean_cb)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  geom_errorbar(aes(ymin=lci_cb, ymax=uci_cb)) +
  scale_y_continuous(labels = scales::percent)



#Try by PID
df4 <- df %>% 
  filter(pair_callback_bin != 2) %>% 
  select(party, callback_binary) %>% 
  group_by(party) %>% 
  summarize(mean_cb = mean(callback_binary), 
            uci_cb = CI(callback_binary, ci = 0.6)[1], 
            lci_cb = CI(callback_binary, ci = 0.6)[3])


## Graph Percentages
ggplot(df4, aes(party, mean_cb)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  geom_errorbar(aes(ymin=lci_cb, ymax=uci_cb)) +
  scale_y_continuous(labels = scales::percent)


#Try by Prestige

df4 <- df %>% 
  filter(party == "NEU") %>% 
  select(prestige, callback_binary) %>% 
  group_by(prestige) %>% 
  summarize(mean_cb = mean(callback_binary), 
            uci_cb = CI(callback_binary)[1], 
            lci_cb = CI(callback_binary)[3])


## Graph Percentages
ggplot(df4, aes(prestige, mean_cb)) +
  #geom_bar(position = "fill") +
  geom_bar(stat = "identity") +
  geom_errorbar(aes(ymin=lci_cb, ymax=uci_cb)) +
  scale_y_continuous(labels = scales::percent)


df_aov <- df %>% 
  mutate(party = as.factor(party)) %>% 
  filter(pair_callback_bin !=2)


df_aov <- df %>% 
  mutate(party = as.factor(party)) %>% 
  filter(pair_callback_bin !=2) %>% 
  filter(wave == "W1")


fit1 <- aov(callback_binary ~ profile, data=df_aov)
summary(fit1)


logit3 <- glm(callback_binary ~ prestige + relevel(party, ref = "NEU"), data = df_aov, family = "binomial")
summary(logit3)



###This is kind of interesting, when 
df_aov <- df %>% 
  mutate(party = as.factor(party)) %>% 
  filter(pair_callback_bin !=2) %>% 
  filter(wave == "W1")

logit1 <- glm(callback_binary ~ prestige + relevel(party, ref = "NEU"), data = df_aov, family = "binomial")
summary(logit1)



df_aov <- df %>% 
  mutate(party = as.factor(party)) %>% 
  #filter(pair_callback_bin !=2) %>% 
  filter(wave == "W1")

logit1 <- glm(callback_binary ~ prestige + relevel(party, ref = "NEU"), data = df_aov, family = "binomial")
summary(logit1)




logit1 <- glm(callback_binary ~ prestige + party, data = df_aov, family = "binomial")
summary(logit1)


