# Working out averages and producing scores:
import pandas as pd
import numpy as np
xml_file = input('enter xml path of part you would like analysed')
full_analysis = pd.read_csv("/Users/NathanWyke/Desktop/python_scripts/Score Analysis/Python/full_analysis_stats.csv")
stat1 = full_analysis[["No. of Notes", "No. Different Note Values"]].describe()
stat2 = full_analysis[["Total Lengths Used", "Average Note Length","Percentage of Notes on First Beat","Percentage of Notes on Weaker Beats","Percentage of Notes on Off Beat"]].describe()
stat3 = full_analysis[["No. Naturals", "No. Accidentals","No. Chords","Total No. of Pitches Used","No. of Octaves Used"]].describe()
stat4 = full_analysis[["No. Pitch Duration Combos", "Average Interval","Maximum Interval"]].describe()
stat5 = full_analysis[["Total No. Bars", "Percentage of bars that are rest","Longest Section of Rest"]].describe()
stat6 = full_analysis[["Overall Total number of repeated fragments", "Overall Total consec. repeats"]].describe()

blank = pd.DataFrame(
        {
         "Song": [np.nan],
         "Instrument":[np.nan],
         "Level": [np.nan],
         
         }
    )
blank2 = pd.DataFrame(
        {
         "Instrument":[np.nan],
         "Level": [np.nan],
         
         }
    )
statfull = pd.concat([blank,stat1,stat2,stat3,stat4,stat5,stat6],axis=1)
print(statfull.head())
# Whole database of songs
stat_data = full_analysis[["Song","Instrument","Level","No. of Notes", "No. Different Note Values","Total Lengths Used",
                           "Average Note Length","Percentage of Notes on First Beat","Percentage of Notes on Weaker Beats",
                           "Percentage of Notes on Off Beat","No. Naturals", "No. Accidentals","No. Chords","Total No. of Pitches Used",
                           "No. of Octaves Used","No. Pitch Duration Combos", "Average Interval","Maximum Interval",
                           "Total No. Bars", "Percentage of bars that are rest","Longest Section of Rest",
                           "Overall Total number of repeated fragments", "Overall Total consec. repeats"]]
useful_data_full = pd.concat([statfull,stat_data])
useful_data_full.to_csv('full_analysis_stats.csv')
#Selected analysed part
selected_part = pd.read_csv('temporary.csv')
selected_stat_data = selected_part[["Instrument","Level","No. of Notes", "No. Different Note Values","Total Lengths Used",
                           "Average Note Length","Percentage of Notes on First Beat","Percentage of Notes on Weaker Beats",
                           "Percentage of Notes on Off Beat","No. Naturals", "No. Accidentals","No. Chords","Total No. of Pitches Used",
                           "No. of Octaves Used","No. Pitch Duration Combos", "Average Interval","Maximum Interval",
                           "Total No. Bars", "Percentage of bars that are rest","Longest Section of Rest",
                           "Overall Total number of repeated fragments", "Overall Total consec. repeats"]]
statfull2 = pd.concat([blank2,stat1,stat2,stat3,stat4,stat5,stat6],axis=1)
useful_data_selected = pd.concat([statfull2,selected_stat_data])
useful_data_selected.to_csv('selected_analysis_stats.csv')


selected_stat_data2 = selected_part[["No. of Notes", "No. Different Note Values","Total Lengths Used",
                           "Average Note Length","Percentage of Notes on First Beat","Percentage of Notes on Weaker Beats",
                           "Percentage of Notes on Off Beat","No. Naturals", "No. Accidentals","No. Chords","Total No. of Pitches Used",
                           "No. of Octaves Used","No. Pitch Duration Combos", "Average Interval","Maximum Interval",
                           "Total No. Bars", "Percentage of bars that are rest","Longest Section of Rest",
                           "Overall Total number of repeated fragments", "Overall Total consec. repeats"]]
selected_data = selected_stat_data2.iloc[0,:]
selected_list = list(selected_data)
print(selected_list)
percentiles = statfull.iloc[:,3:]
median= percentiles.iloc[2,:]
maximum = percentiles.iloc[5,:]
minimum = percentiles.iloc[7,:]
ten = (maximum - median)/5
zeroth = list(minimum)
tenth = list(minimum + ten)
twenty = list(tenth + ten)
thirty = list(twenty + ten)
forty = list(thirty + ten)
fifty = list(median)
sixty = list(median + ten)
seventy = list(sixty + ten)
eighty = list(seventy + ten)
ninty = list(eighty + ten)
hundred = list(maximum)

print(hundred)

score= []
for v in range(len(zeroth)):
    if selected_list[v] >= zeroth[v] and selected_list[v] < tenth[v]:
        score.append(1)
        
    if selected_list[v] >= tenth[v] and selected_list[v] < twenty[v]:
        score.append(2)
    if selected_list[v] >= twenty[v] and selected_list[v] < thirty[v]:
        score.append(3)
    if selected_list[v] >= thirty[v] and selected_list[v] < forty[v]:
        score.append(4)
    if selected_list[v] >= forty[v] and selected_list[v] < fifty[v]:
        score.append(5)
    if selected_list[v] >= fifty[v] and selected_list[v] < sixty[v]:
        score.append(6)
    if selected_list[v] >= sixty[v] and selected_list[v] < seventy[v]:
        score.append(7)
    if selected_list[v] >= seventy[v] and selected_list[v] < eighty[v]:
        score.append(8)
    if selected_list[v] >= eighty[v] and selected_list[v] < ninty[v]:
        score.append(9)
    if selected_list[v] >= ninty[v] and selected_list[v] <= hundred[v]:
        score.append(10)
print(score)
score_quartiles = pd.DataFrame(
    {
        "0%":zeroth,
        "10%":tenth,
        "20%":twenty,
        "30%":thirty,
        "40%":forty,
        "50%":fifty,
        "60%":sixty,
        "70%":seventy,
        "80%":eighty,
        "90%":ninty,
        "100%":hundred,
        "Data":selected_list,
        }
        
    
)
#index = ["No. of Notes", "No. Different Note Values","Total Lengths Used",
                          # "Average Note Length","Percentage of Notes on First Beat","Percentage of Notes on Weaker Beats",
                           #"Percentage of Notes on Off Beat","No. Naturals", "No. Accidentals","No. Chords","Total No. of Pitches Used",
                           #"No. of Octaves Used","No. Pitch Duration Combos", "Average Interval","Maximum Interval",
                          # "Total No. Bars", "Percentage of bars that are rest","Longest Section of Rest",
                          # "Overall Total number of repeated fragments", "Overall Total consec. repeats"]
score = pd.DataFrame(
    {
        "Score":score
    }
)
fullscore = pd.concat([score_quartiles,score],axis=1)        


fullscore.to_csv('selected_analysis_score.csv')
