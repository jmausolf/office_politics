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

source("analysis_source.R")
######################################
## Load Data
######################################

#source file and cleaning

dfec_edit <- dfec %>% 
  mutate(pm_var = pmXf) 
  #filter(matched_pair == "A") %>% 
  #filter(version == "B") 
  #filter(pair_callback_bin != 2) %>%
  #TODO more qc on results, get more results






df2 <- dfec_edit %>% 
  #filter(pair_callback_bin != 2) %>% 
  select(callback_binary, pm_var, party) %>% 
  group_by(pm_var, party) %>% 
  add_tally(callback_binary, name = "total_callbacks") %>% 
  add_count(pm_var, name = "total_applications") %>% 
  mutate(proportion_callback = total_callbacks / total_applications) %>% 
  select(-callback_binary) %>% 
  distinct()

df2

#Get Upper and Lower CI
df2_err <- binconf(df2$total_callbacks, df2$total_applications, alpha=0.05, method=c("asymptotic"))
df2_err <- as.data.frame(df2_err) %>% 
  mutate(pe = PointEst, 
         lci = Lower,
         uci = Upper) %>% 
  select(pe, lci, uci)
df2_full <- bind_cols(df2, df2_err)








df3 <- dfec_edit %>% 
  #filter(pair_callback_bin != 2) %>% 
  select(callback_binary, pm_var) %>% 
  group_by(pm_var) %>% 
  add_tally(callback_binary, name = "total_callbacks") %>% 
  add_count(pm_var, name = "total_applications") %>% 
  mutate(proportion_callback = total_callbacks / total_applications) %>% 
  select(-callback_binary) %>% 
  distinct()


df3

#Get Upper and Lower CI
df3_err <- binconf(df3$total_callbacks, df3$total_applications, alpha=0.05, method=c("asymptotic"))
df3_err <- as.data.frame(df3_err) %>% 
  mutate(pe = PointEst, 
         lci = Lower,
         uci = Upper) %>% 
  select(pe, lci, uci)
df3_full <- bind_cols(df3, df3_err)





party_types <- c(
  "DEM" = "Democrat",
  "NEU" = "Neutral",
  "REP" = "Republican"
)


make_bar_app_match_party <- function(df_in){
  
  g <- ggplot(df_in, aes(pm_var, proportion_callback, fill=pm_var)) +
    geom_bar(stat = "identity") +
    geom_errorbar(aes(ymin=lci, ymax=uci), width=0.4) + 
    facet_grid(~party, labeller = as_labeller(party_types)) +
    
    #Add bbcstyle
    bbc_style() +
    
    scale_y_continuous(labels = scales::percent)  +
    
    scale_fill_manual("", values=colors_parties2) +
    
    #Xaxis Line
    geom_hline(yintercept = 0, size = 1, colour="#333333") +
    
    #Add axis titles
    theme(axis.title = element_text(size = 18)) +
    xlab("Applicant Partisan Match") +
    ylab("Percentage Callbacks") +
    labs(title = "Callbacks by Applicant Party and Partisan Match",
         caption = "") +
    theme(plot.title = element_text(hjust = 0.5)) +
    
    
    #Add x axis ticks
    theme(
      axis.ticks.x = element_line(colour = "#333333"), 
      axis.ticks.length =  unit(0.26, "cm"),
      axis.text = element_text(size=14, color="#222222")) +
    
    theme(
      #Blank Background
      panel.background = ggplot2::element_blank(),
      
      #Grid lines
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major.y = ggplot2::element_line(color="#cbcbcb"),
      panel.grid.major.x = ggplot2::element_blank(),
      
      #Facet Wrap Background
      strip.background = ggplot2::element_rect(fill="white"),
      strip.text = ggplot2::element_text(size  = 18,  hjust = 0.5),
      
      #Axis Text
      axis.text = ggplot2::element_text(size=14,
                                        color="#222222")
    ) +
    
    #Remove Legend
    theme(legend.position = "none")
  #guides(shape = guide_legend(override.aes = list(fill = colors_parties2)))
  
  finalise_plot(g, "", "output/plots/test_bar_partisan_match_X_party_new.png", footer=FALSE)
  return(g)
  
}

make_bar_app_match_party(df2_full)




party_types <- c(
  "DEM" = "Democrat",
  "NEU" = "Neutral",
  "REP" = "Republican"
)


make_bar_app_match_only <- function(df_in){
  
  g <- ggplot(df_in, aes(pm_var, proportion_callback, fill=pm_var)) +
    geom_bar(stat = "identity") +
    geom_errorbar(aes(ymin=lci, ymax=uci), width=0.4) + 
    #facet_grid(~party, labeller = as_labeller(party_types)) +
    
    #Add bbcstyle
    bbc_style() +
    
    scale_y_continuous(labels = scales::percent)  +
    
    scale_fill_manual("", values=colors_grey) +
    
    #Xaxis Line
    geom_hline(yintercept = 0, size = 1, colour="#333333") +
    
    #Add axis titles
    theme(axis.title = element_text(size = 18)) +
    xlab("Applicant Partisan Match") +
    ylab("Percentage Callbacks") +
    labs(title = "Callbacks by Applicant Party and Partisan Match",
         caption = "") +
    theme(plot.title = element_text(hjust = 0.5)) +
    
    
    #Add x axis ticks
    theme(
      axis.ticks.x = element_line(colour = "#333333"), 
      axis.ticks.length =  unit(0.26, "cm"),
      axis.text = element_text(size=14, color="#222222")) +
    
    theme(
      #Blank Background
      panel.background = ggplot2::element_blank(),
      
      #Grid lines
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major.y = ggplot2::element_line(color="#cbcbcb"),
      panel.grid.major.x = ggplot2::element_blank(),
      
      #Facet Wrap Background
      strip.background = ggplot2::element_rect(fill="white"),
      strip.text = ggplot2::element_text(size  = 18,  hjust = 0.5),
      
      #Axis Text
      axis.text = ggplot2::element_text(size=14,
                                        color="#222222")
    ) +
    
    #Remove Legend
    theme(legend.position = "none")
  #guides(shape = guide_legend(override.aes = list(fill = colors_parties2)))
  
  finalise_plot(g, "", "output/plots/test_bar_partisan_match_only_new.png", footer=FALSE)
  return(g)
  
}

make_bar_app_match_only(df3_full)


