####################################################
## Ttests and Loop by Firm
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



