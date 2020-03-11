//Change Directory to Analysis Folder
cd "/Users/Joshua/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/analysis/"

//Make Log Directory If Not Existing
! mkdir log_files || :

//Change Directory to Do Files
cd "/Users/Joshua/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/analysis/log_files"


//Start Log
log using __ttests_analysis.smcl, replace name(__ttests_analysis)

import delimited "/Users/Joshua/Box Sync/Dissertation_v2/CH2_OfficePolitics/office_politics/analysis/ANALYSIS_experiment_results_fec_cleaned.csv", clear




preserve
keep if pmxf != "neutral"
ttest callback_binary, by(pmxf) unequal
restore

preserve
keep if pmxf != "match"
ttest callback_binary, by(pmxf) unequal
restore

preserve
keep if pmxf != "mismatch"
ttest callback_binary, by(pmxf) unequal
restore


preserve
keep if pmxf != "neutral"
keep if partyx == "REP"
ttest callback_binary, by(pmxf) unequal
restore



preserve
keep if pmxf != "neutral"
keep if partyx == "DEM"
ttest callback_binary, by(pmxf) unequal
restore

// Close Log
log close __ttests_analysis
