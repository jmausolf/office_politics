##########################################
## Fixed Party Models
##########################################

#Set Options
# models <- list(m1r, m2r, m3r, m4r)
# ttitle = "Logit Models of the Likelihood that a Job Applicant Receives a Callback at a Republican Firm, Matched Applicants, Odds Ratios Displayed"
# dvar = "Pr\\{Applicant Receives Callback\\}"
# mlabel = "tab:models_main_rep"
# outfile = "output/tables/logit_models_main_republican_firms.tex"
# note_content <- "N = 340. Republican firms only. Matched applicants are those applicants who applied to a firm where the partisanship of the firm could be determined, resulting in three match conditions (mismatch, neutral, and match) based on the partisanship of the firm (Democratic or Republican) and the partisanship of the test applicant (Democratic or Republican) and control applicant (Neutral)."



#Set Options
# models <- list(m1d, m2d, m3d, m4d)
# ttitle = "Logit Models of the Likelihood that a Job Applicant Receives a Callback at a Democratic Firm, Matched Applicants, Odds Ratios Displayed, Only Deduplicated Firms Included"
# dvar = "Pr\\{Applicant Receives Callback\\}"
# mlabel = "tab:models_main_dem"
# outfile = "output/tables/logit_models_main_democratic_firms.tex"
# note_content <- "N = 318. Democratic firms only. Matched applicants are those applicants who applied to a firm where the partisanship of the firm could be determined, resulting in three match conditions (mismatch, neutral, and match) based on the partisanship of the firm (Democratic or Republican) and the partisanship of the test applicant (Democratic or Republican) and control applicant (Neutral)."



#asr
r = 23
r2 = 27
d = 3


#Add Insert Row Function
insertrow <- function(existingDF, newrow, r) {
  existingDF[seq(r+1,nrow(existingDF)+1),] <- existingDF[seq(r,nrow(existingDF)),]
  existingDF[r,] <- newrow
  existingDF
}

# Create some standard rows to add.
hline <- "\\hline"
hline2 <- "\\hline \\\\[-1.8ex]"
newline <- "\\\\"
newline_space <- "\\\\[-1em]"
blankline <- " & & & & \\\\"

# Make Note
note_form <- "\\multicolumn{5}{l}{\\parbox[t]{0.9\\textwidth}{{\\textit{Notes:}}"
tnote <- paste(note_form, note_content, "}}", "\\\\", sep=" ")
tnote



m1 = models[[1]]
m2 = models[[2]]
m3 = models[[3]]
m4 = models[[4]]


#make base tables
tables <- stargazer2(models,
                     odd.ratio = T,
                     star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
                     star.char = c("+", "*", "**", "***"),
                     notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"),
                     align = TRUE,
                     initial.zero = TRUE,
                     # no.space = TRUE,
                     column.sep.width = "0pt",
                     header = FALSE,
                     font.size = "scriptsize",
                     style = "asr",
                     title = ttitle,
                     dep.var.labels   = dvar,
                     label = mlabel,
                     covariate.labels = c("\\textit{Applicant Partisan Matching} \\\\Mismatched Partisan",
                                          "Neutral Applicant",

                                          "\\\\ \\textit{Applicant Prestige} \\\\ High Prestige",
                                          
                                          
                                          "\\\\ \\textit{Job Type} \\\\ MS: Computer Scientist",
                                          "MBA: Analyst or Manager",

                                          "\\\\ \\textit{Region} \\\\ Midwest",
                                          "South",
                                          "West Coast",
                                          
                                          "\\\\ \\textit{Experiment Features} \\\\ Received Order: Second",
                                          "Resume Version: B",
                                          "Experiment Wave: Second Wave",
                                          "Constant"),
                     notes.append = FALSE, notes.align = "l"
                     )

tables <- as.data.frame(tables)
tables$tables <- as.character(tables$tables)
tables

#Add Table Note
tables <- insertrow(tables, tnote, r2)

#Add Hline Before N
tables <- insertrow(tables, hline2, r)

# Reference Groups
ref_pm <- "(Ref: Matched Partisan) \\\\"
ref_firm <- "(Ref: Republican Firm) \\\\"
ref_prestige <- "(Ref: Lower Prestige) \\\\"
ref_job <- "(Ref: Ph.D. Data Scienctist-Quant) \\\\"
ref_region <- "(Ref: East Coast) \\\\"

#Add Reference Group Rows
tables <- insertrow(tables, ref_pm, 13)
tables <- insertrow(tables, ref_firm, 15)
tables <- insertrow(tables, ref_prestige, 17)
tables <- insertrow(tables, ref_job, 20)
tables <- insertrow(tables, ref_region, 24)


write.table(tables,file=outfile,sep="",row.names= FALSE,na="", quote = FALSE, col.names = FALSE)
