# -*- coding: utf-8 -*-
"""
Created on Apr 22 2021
Code to process Repetition Information from xml part
@author: Cameron Wyke
"""

#################################################################
from music21 import *
import statistics
import numpy as np
import pandas as pd
import os
from os import path
import time

######################## User Entry ###################################
def rep_analysis(part, bars_total):
#REPETITION

    # 2 bar fragments
    def searchRepetition(repeat_length):
        #half_bars_total = int(bars_total/repeat_length)
        bar_start = []
        for i in range(1,int(bars_total-repeat_length+1)):
            bar_start.append(i)
        #print(bar_start)
        dict_2 = {}
        for i in bar_start:
            excerpt = part.measures(i,i+(repeat_length-1))
            excerpt_notes=[]
            for note in excerpt.flat.notesAndRests:
                excerpt_notes.append(note)

            if i not in dict_2:
                #gets rid of case where section is all rests
                result = all(elem.isRest == True for elem in excerpt_notes)
                if result == False:

                    dict_2[i] = excerpt_notes
        no_repetitions_dict = {}
        bars_where_repeated_dict = {}
        for i in dict_2:
            if i not in no_repetitions_dict:
                no_repetitions_dict[i] = 0
            if i not in bars_where_repeated_dict:
                bars_where_repeated_dict[i] = []
            for j in dict_2:
                if i != j and dict_2[i] == dict_2[j]:
                    bars_where_repeated_dict[i].append(j)
                    no_repetitions_dict[i] += 1

        #create copy of dict so can delete repeated items
        repeated_bars_new = bars_where_repeated_dict.copy()
        key_fragments = []

        key_index = 0
        key_indexdict= {}
        for k, v in bars_where_repeated_dict.items():
            key_index += 1
            if k not in key_indexdict:
                key_indexdict[key_index]= k
            if k not in key_fragments:
                key_fragments.append(k)
            if any(bar in key_fragments for bar in v) == True:
                del repeated_bars_new[k]
            if v == []:
                del repeated_bars_new[k]
            repeated_bars_new_2 = repeated_bars_new.copy()
        for i in key_indexdict:
            if i != 1:
                key = key_indexdict[i]
                bars = bars_where_repeated_dict[key]
                last_key = key_indexdict[i-1]
                last_bars = bars_where_repeated_dict[last_key]
                test = [bar + 1 for bar in last_bars]
                if bars == test:
                    if key in repeated_bars_new and last_key in repeated_bars_new:
                        del repeated_bars_new_2[key]
                    #del repeated_bars_new[last_key]
        return dict_2, no_repetitions_dict, bars_where_repeated_dict, repeated_bars_new_2



    half_bars_total = int(bars_total/2)
    bar_start = []
    #2 is repeat length - repeat length +1
    for i in range(1,int(bars_total-2+1)):
        bar_start.append(i)
    #print(bar_start)
    dict_2 = {}
    for i in bar_start:
        excerpt = part.measures(i,i+1)
        excerpt_notes=[]
        for note in excerpt.flat.notesAndRests:
            excerpt_notes.append(note)

        if i not in dict_2:
            #gets rid of case where section is all rests
            result = all(elem.isRest == True for elem in excerpt_notes)
            if result == True:
                dict_2[i] = []
            else:
                dict_2[i] = excerpt_notes
    no_repetitions_dict = {}
    bars_where_repeated_dict = {}
    for i in dict_2:
        if i not in no_repetitions_dict:
            no_repetitions_dict[i] = 0
        if i not in bars_where_repeated_dict:
            bars_where_repeated_dict[i] = []
        for j in dict_2:
            if i != j and dict_2[i] == dict_2[j] and dict_2[i] != []:
                bars_where_repeated_dict[i].append(j)
                no_repetitions_dict[i] += 1
    #create copy of dict so can delete repeated items
    repeated_bars_new = bars_where_repeated_dict.copy()
    key_fragments = []
    #print(len(key_fragments))
    key_index = 0
    key_indexdict= {}
    for k, v in bars_where_repeated_dict.items():
        key_index += 1
        if k not in key_indexdict:
            key_indexdict[key_index]= k
        if k not in key_fragments:
            key_fragments.append(k)
        if any(bar in key_fragments for bar in v) == True:
            del repeated_bars_new[k]
        if v == []:
            del repeated_bars_new[k]
    for i in key_indexdict:
        if i != 1:
            key = key_indexdict[i]
            bars = bars_where_repeated_dict[key]
            last_key = key_indexdict[i-1]
            last_bars = bars_where_repeated_dict[last_key]
            test = [bar + 1 for bar in last_bars]
            if bars == test:
                if key in repeated_bars_new and last_key in repeated_bars_new:
                    del repeated_bars_new[key]
                    #del repeated_bars_new[last_key]






    #search through piece for 2 bar repetition
    dict_list = searchRepetition(2)
    dict_excerpt_2, no_repetitions_dict,bars_where_repeated_dict, bars_repeated_edited = dict_list


    def sort_trim(bars_repeated_edited, under_eight = True):
        sorted_final = sorted(bars_repeated_edited, reverse= True, key= lambda k: len(bars_repeated_edited[k]))

        sorted_final_dict = {}
        for k in sorted_final:
            values = bars_repeated_edited[k]
            if under_eight == True:
                if len(values) != 1:
                    if k not in sorted_final_dict:
                        sorted_final_dict[k] = values
            else:
                 if k not in sorted_final_dict:
                        sorted_final_dict[k] = values
        return sorted_final_dict

    #print(bars_repeated_edited)
    sorted_final_dict_2 = sort_trim(bars_repeated_edited)
    #print(sorted_final_dict_2)

    #search through piece for 4 bar repetition
    dict_list = searchRepetition(4)
    dict_excerpt_4, no_repetitions_dict, bars_where_repeated_dict, bars_repeated_edited = dict_list
    #print(bars_repeated_edited)
    sorted_final_dict_4 = sort_trim(bars_repeated_edited)
    #print(sorted_final_dict_4)

    #search through piece for 8 bar repetition
    dict_list = searchRepetition(8)
    dict_excerpt_8, no_repetitions_dict,bars_where_repeated_dict, bars_repeated_edited = dict_list

    #print(bars_repeated_edited)
    sorted_final_dict_8 = sort_trim(bars_repeated_edited, under_eight = False)
    #print(sorted_final_dict_8)

    # see whether 2, 4 or 8 bar pattern
    final_dict_2 = sorted_final_dict_2.copy()
    final_dict_4 = sorted_final_dict_4.copy()
    final_dict_8 = sorted_final_dict_8.copy()
    for k in sorted_final_dict_2:
        if k in sorted_final_dict_4:
            #check if 2 bar *2 = 4 bar
            excerpt_repeated = dict_excerpt_2[k] * 2
            if excerpt_repeated == dict_excerpt_4[k]:
                del final_dict_4[k]
                if k in sorted_final_dict_8:
                    del final_dict_8[k]
            else:
                del final_dict_2[k]
    # same for 4 bar
    for k in sorted_final_dict_4:
        if k in sorted_final_dict_8:
            #check if 2 bar *2 = 4 bar
            excerpt_repeated = dict_excerpt_4[k] * 2
            if excerpt_repeated == dict_excerpt_8[k]:

                del final_dict_8[k]
            else:
                del final_dict_4[k]
    # FINAL SORTED DICTIONARIES
    #print(final_dict_2, '\n', final_dict_4, '\n', final_dict_8)


    #SEARCH TO SEE HOW MANY CONSECUTIVE REPEATS OF FRAGMENT
    def find_consecutive_repeats(sorted_final_dict, repeat_length):
        no_consec_dict = {}
        for k in sorted_final_dict:
            if k not in no_consec_dict:
                no_consec_dict[k] = 0
            v = sorted_final_dict[k]
            if k + repeat_length == v[0]:
                no_consec_dict[k] += 1
            for n in range(len(v)):
                if (v[n] - repeat_length) == v[n-1] and n!= v[0]:
                    no_consec_dict[k] += 1
        return no_consec_dict
    # 2 bar:
    consec_2bar = find_consecutive_repeats(final_dict_2, 2)

    # 4 bar
    consec_4bar = find_consecutive_repeats(final_dict_4, 4)

    # 8 bar
    consec_8bar = find_consecutive_repeats(final_dict_8, 8)

    #print(consec_2bar)
    #print(consec_4bar)
    #print(consec_8bar)
    def print_repeat_info(final_dict, consec_dict, repeat_length):
        repeat_startbars = []
        bars_repeated_at = []
        no_consec_repeats = []
        length_fragment = []
        for k in final_dict:
            print('{} bar fragment at bar {} repeats at bars {}, {} consecutive repeats'.format(repeat_length, k, final_dict[k], consec_dict[k]))
            length_fragment.append(repeat_length)
            repeat_startbars.append(k)
            bars_repeated_at.append(final_dict[k])
            no_consec_repeats.append(consec_dict[k])
        dfrepeat = pd.DataFrame(
            {
                "Length of Repeat Fragment" : length_fragment,
                "Fragment Start Bar": repeat_startbars,
                "Where Else Repeated": bars_repeated_at,
                "Consecutive Repeats": no_consec_repeats,
            }
        )
        total_consec_repeats = 0
        for n in no_consec_repeats:
            total_consec_repeats += n
        no_repeats = 0
        for b in bars_repeated_at:
            no_repeats += (len(b)+1)


        return dfrepeat, no_repeats, total_consec_repeats
    dfrepeat2, no_repeats2, total_consec_repeats2 = print_repeat_info(final_dict_2, consec_2bar, 2)
    dfrepeat4, no_repeats4, total_consec_repeats4 = print_repeat_info(final_dict_4, consec_4bar, 4)
    dfrepeat8, no_repeats8, total_consec_repeats8 = print_repeat_info(final_dict_8, consec_8bar, 8)
    blank = pd.DataFrame(
        {" ": [np.nan]}
    )
    no_repeats_total = no_repeats2 + no_repeats4 + no_repeats8
    total_consec_repeats = total_consec_repeats2 + total_consec_repeats4 + total_consec_repeats8
    df2 = pd.DataFrame(
        {
            "Total number of 2 bar repeated fragments" : [no_repeats2],
            "Total number of 4 bar repeated fragments" : [no_repeats4],
            "Total number of 8 bar repeated fragments" : [no_repeats8],
            "Overall Total number of repeated fragments" : [no_repeats_total],
            "Total 2 bar consec. repeats" : [total_consec_repeats2],
            "Total 4 bar consec. repeats" : [total_consec_repeats4],
            "Total 8 bar consec. repeats" : [total_consec_repeats8],
            "Overall Total consec. repeats" : [total_consec_repeats]
        }
    )

    dfrep = pd.concat([dfrepeat2,dfrepeat4,dfrepeat8,df2], axis=1)
    return dfrep
