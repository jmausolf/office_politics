library(gtools)

####################################################
## Ttests Loop by Firm and Match
####################################################

#Ttest Loop, Print Results
party_matches <- c("mismatch", "neutral", "match")
parties <- c("DEM", "REP")
output_ttest <- list()
for(i in seq_along(parties)){
  for(j in seq_along(party_matches)){
    p = parties[i]
    pm = party_matches[j]
    id <- paste(p, pm, sep = '_')
    ttd <- dfec %>% select(callback_binary, partyX, pmXf) %>% filter(pmXf != pm, partyX == p)
    tt <- t.test(callback_binary~pmXf, data = ttd)
    
    print(p)
    print(tt)
    
  }
}


tWrap <- function(x) t.test(x$Var1, x$Var2)$p.value

df_ttests <- dfec %>% select(callback_binary, pmXf, partyX) %>% filter(partyX == "REP")
L <- split(df_ttests$callback_binary, df_ttests$pmXf)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=3)
pval_rep <- pvals_mat
pval_df_rep <- as.data.frame(pval_rep)
colnames(pval_df_rep) <- c('pval1', 'pval2', 'pval3')
rownames(pval_df_rep) <- c('mismatch_REP', 'neutral_REP', 'match_REP')
pval_df_rep$pm_var_party = rownames(pval_df_rep)


df_ttests <- dfec %>% select(callback_binary, pmXf, partyX) %>% filter(partyX == "DEM")
L <- split(df_ttests$callback_binary, df_ttests$pmXf)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=3)
pval_dem <- pvals_mat
pval_df_dem <- as.data.frame(pval_dem)
colnames(pval_df_dem) <- c('pval1', 'pval2', 'pval3')
rownames(pval_df_dem) <- c('mismatch_DEM', 'neutral_DEM', 'match_DEM')
pval_df_dem$pm_var_party = rownames(pval_df_dem)

pval_ttests <- bind_rows(pval_df_rep, pval_df_dem)
pval_ttests


#library(gtools)
pval_df1 <- pval_ttests %>% 
  mutate(stars1 = stars.pval(pval1)) %>% 
  mutate(stars2 = stars.pval(pval2)) %>% 
  mutate(stars3 = stars.pval(pval3)) %>% 
  mutate(star_range1 = paste(stars1, ' ^ ', stars2, sep = '')) %>%
  mutate(star_range2 = paste(stars1, ' ^ ', stars3, sep = '')) %>%
  mutate(star_range3 = paste(stars2, ' ^ ', stars3, sep = '')) %>% 


  mutate(star_range1 = ifelse( stars1 == " " | stars2 == " ", "", star_range1)) %>% 
  mutate(star_range2 = ifelse( stars1 == " " | stars3 == " ", "", star_range2)) %>%
  mutate(star_range3 = ifelse( stars2 == " " | stars3 == " ", "", star_range3)) %>% 
  
  mutate(star_range = paste0(star_range1, star_range2, star_range3)) %>% 
  select(pm_var_party, star_range, pval1, pval2, pval3) %>% 
  filter(!(pm_var_party == "neutral_DEM" | pm_var_party == "match_DEM"))

pval_df1


pval_df2 <- pval_ttests %>% 
  mutate(stars1 = stars.pval(pval1)) %>% 
  mutate(stars2 = stars.pval(pval2)) %>% 
  mutate(stars3 = stars.pval(pval3)) %>% 
  mutate(star_range1 = paste( stars1, ' ^ ', stars2, sep = '')) %>%
  mutate(star_range2 = paste( stars1, ' ^ ', stars3, sep = '')) %>%
  mutate(star_range3 = paste( stars2, ' ^ ', stars3, sep = '')) %>% 
  mutate(star_range = star_range1) %>% 
  select(pm_var_party, star_range, pval1, pval2, pval3) %>% 
  filter(pm_var_party == "neutral_DEM" | pm_var_party == "match_DEM")

pval_df2

pvals_df_firm <- rbind(pval_df1, pval_df2)
pvals_df_firm


####################################################
## Ttests Loop by Match
####################################################


#Ttest Loop, Print Results
party_matches <- c("mismatch", "neutral", "match")
output_ttest <- list()
for(i in seq_along(party_matches)){
    pm = party_matches[i]
    ttd <- dfec %>% select(callback_binary, partyX, pmXf) %>% filter(pmXf != pm)
    tt <- t.test(callback_binary~pmXf, data = ttd)
    
    print(tt)
}


tWrap <- function(x) t.test(x$Var1, x$Var2)$p.value

df_ttests <- dfec %>% select(callback_binary, pmXf, partyX) 
L <- split(df_ttests$callback_binary, df_ttests$pmXf)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=3)
pval_pm <- pvals_mat
pval_df_pm <- as.data.frame(pval_pm)
pval_df_pm
colnames(pval_df_pm) <- c('pval1', 'pval2', 'pval3')
rownames(pval_df_pm) <- c('mismatch', 'neutral', 'match')
pval_df_pm$pm_var = rownames(pval_df_pm)
pval_df_pm


#library(gtools)
pvals_df_matches <- pval_df_pm %>% 
  mutate(stars1 = str_replace(stars.pval(pval1), '\\.', '+')) %>% 
  mutate(stars2 = str_replace(stars.pval(pval2), '\\.', '+')) %>% 
  mutate(stars3 = str_replace(stars.pval(pval3), '\\.', '+')) %>% 


  mutate(star_range1 = paste(stars1, ' ^ ', stars2, sep = '')) %>%
  mutate(star_range2 = paste(stars1, ' ^ ', stars3, sep = '')) %>%
  mutate(star_range3 = paste(stars2, ' ^ ', stars3, sep = '')) %>% 


  mutate(star_range1 = ifelse( stars1 == " " | stars2 == " ", "", star_range1)) %>% 
  mutate(star_range2 = ifelse( stars1 == " " | stars3 == " ", "", star_range2)) %>%
  mutate(star_range3 = ifelse( stars2 == " " | stars3 == " ", "", star_range3)) %>% 
  
  mutate(star_range = paste0(star_range1, star_range2, star_range3)) %>% 
  select(pm_var, star_range, pval1, pval2, pval3) 

pvals_df_matches



####################################################
## Ttests Loop by App Party
####################################################


#Ttest Loop, Print Results
parties <- c("DEM", "REP")
output_ttest <- list()
for(i in seq_along(parties)){
  p = parties[i]
  ttd <- dfec %>% select(callback_binary, party, pmXf) %>% filter(pmXf != 'neutral', party==p)
  tt <- t.test(callback_binary~pmXf, data = ttd)
  
  print(p)
  print(tt)
}


tWrap <- function(x) t.test(x$Var1, x$Var2)$p.value

#Get Dem App Results
df_ttests <- dfec %>% select(callback_binary, pmXf, party) %>% 
  filter(pmXf != 'neutral', party == 'DEM') %>% 
  mutate(pmXf = factor(pmXf, levels = c('mismatch', 'match')))
L <- split(df_ttests$callback_binary, df_ttests$pmXf)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=2)
pval_pm <- pvals_mat
pval_df_pm_dem <- as.data.frame(pval_pm)
colnames(pval_df_pm_dem) <- c('pval1', 'pval2')
rownames(pval_df_pm_dem) <- c('mismatch', 'match')
pval_df_pm_dem$pm_var = rownames(pval_df_pm_dem)
pval_df_pm_dem$party = 'DEM'

#Get Rep App Results
df_ttests <- dfec %>% select(callback_binary, pmXf, party) %>% 
  filter(pmXf != 'neutral', party == 'REP') %>% 
  mutate(pmXf = factor(pmXf, levels = c('mismatch', 'match')))
L <- split(df_ttests$callback_binary, df_ttests$pmXf)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=2)
pval_pm <- pvals_mat
pval_df_pm_rep <- as.data.frame(pval_pm)
pval_df_pm_rep <- as.data.frame(pval_pm)
colnames(pval_df_pm_rep) <- c('pval1', 'pval2')
rownames(pval_df_pm_rep) <- c('mismatch', 'match')
pval_df_pm_rep$pm_var = rownames(pval_df_pm_rep)
pval_df_pm_rep$party = 'REP'

#Join and Get Stars
pval_df_pm_party <- bind_rows(pval_df_pm_dem, pval_df_pm_rep)
pvals_df_matches_party <- pval_df_pm_party %>% 
  mutate(stars1 = str_replace(stars.pval(pval1), '\\.', '+')) %>% 
  mutate(stars2 = str_replace(stars.pval(pval2), '\\.', '+')) %>% 

  mutate(stars1 = ifelse( stars1 == " ", "", stars1)) %>% 
  mutate(stars2 = ifelse( stars2 == " ", "", stars2)) %>% 
  
  mutate(star_range = paste(stars1, stars2, sep = '')) %>%
  mutate(pm_var = factor(pm_var, labels = c("MISMATCH", "MATCH"))) %>% 
  select(pm_var, party, star_range, pval1, pval2) 

pvals_df_matches_party



####################################################
## Ttests Loop by App Party Only (Unmatched)
####################################################


#Ttest Loop, Print Results (by Party)
parties <- c("DEM", "NEU", "REP")
output_ttest <- list()
for(i in seq_along(parties)){
    p = parties[i]
    id <- paste(p, pm, sep = '_')
    ttd <- dfa %>% select(callback_binary, party) %>% filter(party != p)
    tt <- t.test(callback_binary~party, data = ttd)
    
    print(tt)

}

#Ttest Prestige
tt <- t.test(callback_binary~prestige_level, data = dfa)
print(tt)


#Ttest Loop, Print Results (by Party and Prestige)
parties <- c("DEM", "NEU", "REP")
prestige <- c("High", "Low")
output_ttest <- list()
for(i in seq_along(parties)){
  for(j in seq_along(prestige)){
    p = parties[i]
    pr = prestige[j]
    
    #print(p, pr)
    id <- paste(p, pr, sep = '_')
    ttd <- dfa %>% select(callback_binary, party, prestige_level) %>% filter(party != p, prestige_level == pr)
    tt <- t.test(callback_binary~party, data = ttd)
    
     print(pr)
     print(tt)
    
  }
}


tWrap <- function(x) t.test(x$Var1, x$Var2)$p.value

df_ttests <- dfa %>% select(callback_binary, party, prestige_level) %>% filter(prestige_level == "High")
L <- split(df_ttests$callback_binary, df_ttests$party)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=3)
pval_high <- pvals_mat
pval_df_high <- as.data.frame(pval_high)
colnames(pval_df_high) <- c('pval1', 'pval2', 'pval3')
rownames(pval_df_high) <- c('DEM_High', 'NEU_High', 'REP_High')
pval_df_high$party_prestige = rownames(pval_df_high)


df_ttests <- dfa %>% select(callback_binary, party, prestige_level) %>% filter(prestige_level == "Low")
L <- split(df_ttests$callback_binary, df_ttests$party)
pvals <- apply(expand.grid(L, L), 1, tWrap)
pvals_mat <- matrix(pvals, ncol=3)
pval_low <- pvals_mat
pval_df_low <- as.data.frame(pval_low)
colnames(pval_df_low) <- c('pval1', 'pval2', 'pval3')
rownames(pval_df_low) <- c('DEM_Low', 'NEU_Low', 'REP_Low')
pval_df_low$party_prestige = rownames(pval_df_low)

pval_ttests <- bind_rows(pval_df_high, pval_df_low)
pval_ttests


#library(gtools)
pval_df_party_prestige <- pval_ttests %>% 
  mutate(stars1 = stars.pval(pval1)) %>% 
  mutate(stars2 = stars.pval(pval2)) %>% 
  mutate(stars3 = stars.pval(pval3)) %>% 
  
  mutate(stars1 = ifelse( stars1 == " ", "", stars1)) %>% 
  mutate(stars2 = ifelse( stars2 == " ", "", stars2)) %>% 
  mutate(stars3 = ifelse( stars3 == " ", "", stars3)) %>% 
  
  mutate(star_range1 = paste(stars1, ' ^ ', stars2, sep = '')) %>%
  mutate(star_range2 = paste(stars1, ' ^ ', stars3, sep = '')) %>%
  mutate(star_range3 = paste(stars2, ' ^ ', stars3, sep = '')) %>% 

  mutate(star_range = star_range2) %>% 
  mutate(star_range = ifelse( star_range == ' ^ ', "", star_range)) %>% 
  select(party_prestige, star_range, pval1, pval2, pval3) 

pval_df_party_prestige

