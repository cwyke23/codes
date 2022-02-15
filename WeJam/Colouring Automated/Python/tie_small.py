# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:03:29 2020

@author: arvin
"""
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


div_list = [32, 16, 8, 4, 2, 1]
div_list_dot = []
div_list_2dot = []
div_list_3dot = []
true_div = []
dot = []; two_dot = []; three_dot = []

for i in range(len(div_list)):
    div = (div_list[i])
    dot.append(div/2)
    two_dot.append(div/4)
    three_dot.append(div/8)
    div_list_dot.append(div+div/2)
    div_list_2dot.append(div + div/2 + div/4)
    div_list_3dot.append(div + div/2 + div/4 + div/8)
    true_div.append(div)
    true_div.append(div+div/2)
all_div = sorted(div_list + div_list_dot + div_list_2dot + div_list_3dot, reverse = True)
true_div =  sorted(true_div, reverse = True)
true_div.pop(0)


def tie_check(start_note, note_div, sig, three = False):
    time_sig = sig.split('/')
    beats_per_bar = int(time_sig[0])
    beat_note = int(time_sig[1])    
    bar_diff = False   
    found = False 
    tie = False
    #note_div = 40
    div_bar = ((32/beat_note)*beats_per_bar) * (beat_note/4)
    diff = div_bar - start_note
    nan = float('nan')
    if diff < note_div:
        tie = True
        bar_diff = True
    else:    
        if note_div in true_div:
            tie = False
            #print('The note length is {} divs and it is a not a tie!'.format(note_div))
        else:
            tie = True
            #print('The note length is {} divs and it is likely to be a tie!'.format(note_div))   

    if tie == True:
            diff = div_bar - start_note
            if bar_diff == True:
                first =  div_bar - start_note
                second = note_div - first
                if second > div_bar:
                    third = second - div_bar
                    second = div_bar
                    three = True
                    return first, second, third, tie, bar_diff, three
                else:
                    return first, second, tie, bar_diff, three
    else:
             return 0, 0, 0, 0, 0
#    tie_check(i)
#try:
#    first, second, tie, bar_diff = tie_check(24, 48)
#except:
#    first, second, third, tie, bar_diff = tie_check(24, 48) 
#tie_check(0,64, '6/8')