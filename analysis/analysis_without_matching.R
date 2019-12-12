######################################
## Load Libraries & Data
######################################


library(Rmisc)
library(Hmisc)
library(tidyverse)
library(bbplot)
library(scales)
library(RColorBrewer)
library(ggthemes)


colors_neutral = rev(brewer.pal(n = 8, name = "Purples")[5:8])
colors_dem = rev(brewer.pal(n = 8, name = "Blues")[5:8])
colors_rep = c("#700009", "#99000D", "#D80012", "#EF3B2C")

colors_grey = rev(brewer.pal(n = 8, name = "Greys")[5:8])
show_col(colors_grey)

colors_parties2 = c("#2129B0", "#969696", "#BF1200")
colors_parties1 = c(colors_dem[1], colors_neutral[1], colors_rep[1])
colors_parties0 = c("#2129B0", "#3A084A", "#BF1200")
show_col(colors_parties0)

#Display a Pallete
show_col(colors_dem)

#Overwrite bbplot finalise_plot() function
source("bb_finalise_plot_academic.R")


######################################
## Load Data
######################################


df <- read_csv("ANALYSIS_experiment_results.csv")
#df <- read_csv("ANALYSIS_experiment_results_with_bounces_errors.csv")
print(df)
table(df$profile, df$callback_binary)
#df <- df %>% 
  #select(callback_binary, profile, company, pair_callback_bin) %>% 
#  filter(callback_binary >= 1) 

#   filter(matched_pair == "A")



#df <- read_csv("ANALYSIS_experiment_results_fec.csv")
#table(df_fec$profile, df_fec$callback_binary)


df2 <- df %>% 
  #filter(pair_callback_bin != 2) %>% 
  select(profile, callback_binary, prestige, party) %>% 
  group_by(profile) %>% 
  add_tally(callback_binary, name = "total_callbacks") %>% 
  add_count(profile, name = "total_applications") %>% 
  mutate(proportion_callback = total_callbacks / total_applications) %>% 
  select(-callback_binary) %>% 
  distinct()


#Get Upper and Lower CI
df2_err <- binconf(df2$total_callbacks, df2$total_applications, alpha=0.05, method=c("wilson"))
df2_err <- as.data.frame(df2_err) %>% 
  mutate(pe = PointEst, 
         lci = Lower,
         uci = Upper) %>% 
  select(pe, lci, uci)
df2_full <- bind_cols(df2, df2_err)


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
  scale_y_continuous(labels = scales::percent)  +

  #Xaxis Line
  geom_hline(yintercept = y_int, size = 1, colour="#333333") +
  
  #Add axis titles
  theme(axis.title = element_text(size = 18)) +
  xlab("Contribution Cycle") +
  ylab(y_axis_lab) +
  labs(title = plt_title,
       caption = plt_caption) +
  theme(plot.title = element_text(hjust = 0.5)) +
  
  #Adjust Legend Position
  theme(
    legend.spacing.x = unit(2.0, 'mm'),
    legend.text = element_text(size=18)
  ) +
  
  #Add x axis ticks
  theme(
    axis.ticks.x = element_line(colour = "#333333"), 
    axis.ticks.length =  unit(0.26, "cm"),
    axis.text = element_text(size=14, color="#222222")) +
  
  #Override the Legend Fill
  guides(shape = guide_legend(override.aes = list(fill = colors_vec)))



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


