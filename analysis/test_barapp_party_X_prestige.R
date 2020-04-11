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

show_col(brewer.pal.all())

#Display a Pallete
show_col(colors_dem)

colors(colors_dem)
plot(colors_dem)

show_col(colors_dem)

showCols(colors_dem)
display.pal(colors_dem)
display.brewer.pal(n = 4, name = 'colors_dem')

scale_color_manual("", values=colors_vec, labels=occ_labels)

#Overwrite bbplot finalise_plot() function
source("bb_finalise_plot_academic.R")


######################################
## Load Data
######################################


df <- read_csv("ANALYSIS_experiment_results.csv")
#df <- read_csv("ANALYSIS_experiment_results_with_bounces_errors.csv")
print(df)

#df <- df %>% 
#select(callback_binary, profile, company, pair_callback_bin) %>% 
#  filter(callback_binary >= 1) 

#   filter(matched_pair == "A")




table(df$profile, df$callback_binary)


prestige_types <- c(
  "H" = "High Prestige",
  "L" = "Low Prestige"
)

party_types <- c(
  "DEM" = "Democrat",
  "NEU" = "Neutral",
  "REP" = "Republican"
)


make_barapp_party_X_prestige <- function(df_in, outid="test123"){

  outfile <- wout("barapp_party_X_prestige", outid)


  prestige_types <- c(
    "H" = "High Prestige",
    "L" = "Low Prestige"
  )

  dfg <- df_in %>% 
    #filter(pair_callback_bin != 2) %>% 
    select(callback_binary, profile, party, prestige) %>% 
    group_by(profile) %>% 
    add_tally(callback_binary, name = "total_callbacks") %>% 
    add_count(profile, name = "total_applications") %>% 
    mutate(proportion_callback = total_callbacks / total_applications) %>% 
    #mutate(uci_cb = binconf(total_callbacks, total_applications, alpha=0.05)) %>% 
    select(-callback_binary) %>% 

    #sort(profile) %>% 
    distinct()


  #Get Upper and Lower CI
  dfg_err <- binconf(dfg$total_callbacks, dfg$total_applications, alpha=0.05, method=c("wilson"))
  dfg_err <- as.data.frame(dfg_err) %>% 
    mutate(pe = PointEst, 
           lci = Lower,
           uci = Upper) %>% 
    select(pe, lci, uci)
  dfg_full <- bind_cols(dfg, dfg_err)



  
  g <- ggplot(dfg_full, aes(party, proportion_callback, fill=party)) +
    geom_bar(stat = "identity") +
    geom_errorbar(aes(ymin=lci, ymax=uci), width=0.4) + 
    facet_grid(~prestige, labeller = as_labeller(prestige_types)) +
    
    #Add bbcstyle
    bbc_style() +
    
    scale_y_continuous(labels = scales::percent)  +
    
    scale_fill_manual("", values=colors_parties2) +
    
    #Xaxis Line
    geom_hline(yintercept = 0, size = 1, colour="#333333") +
    
    #Add axis titles
    theme(axis.title = element_text(size = 18)) +
    xlab("Applicant Political Party") +
    ylab("Percentage Callbacks") +
    labs(title = "Callbacks by Applicant Party and Prestige",
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
  
    finalise_plot(g, "", outfile, footer=FALSE)
    #return(g)

    return(dfg_full)
    
}

x <- make_barapp_party_X_prestige(df)

#x <- make_bar_app_prestige_party(df, "profile")
#x2 <- make_bar_app_prestige_party(df, "party")

