# -*- coding: utf-8 -*-
"""
Created on Apr 22 2021
Code to process Rest and Playing time Information from xml part
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
def rest_analysis(part):
    #RESTS
    # percentage bars rest
    total_length = 0
    rest_length = 0
    resting_list = []
    playing_list = []
    for n in part.flat.notesAndRests:
        #print(n.isRest)
        total_length = total_length + n.duration.quarterLength
        if n.isRest == True:
            rest_length = rest_length + n.duration.quarterLength

    #print(total_length, rest_length, '***')
    percentage_rest = int((rest_length/total_length)*100)

    #set time sig
    a = part.getTimeSignatures()
    b = str(a.timeSignature)
    print(b[-4:-1])

    #time_sig = input('Time Signature?')
    time_sig = b[-4:-1]
    list_sig = time_sig.split('/')
    #how many quarter notes in a bar
    quarter_in_bar = int(list_sig[0])*(1/int(list_sig[1]))*4
    part.timeSignature = meter.TimeSignature(time_sig)
    bars_rest = rest_length/quarter_in_bar
    bars_total = total_length/quarter_in_bar
    bars_play = bars_total - bars_rest
    print('Total bars: {}, bars rest: {}, \
    total percentage rest in part is {} %'.format(bars_total,bars_rest,percentage_rest))

    #sections of rest/play and maximum period of rest
    length_counter = 0
    section_length = []
    section_type = []
    for n in range(len(part.flat.notesAndRests)):
        if n != 0:
            if part.flat.notesAndRests[n].isRest == part.flat.notesAndRests[n-1].isRest:
               length_counter += part.flat.notesAndRests[n-1].duration.quarterLength
            elif n == len(part.flat.notesAndRests):
                if  part.flat.notesAndRests[n].isRest == part.flat.notesAndRests[n-1].isRest:
                    length_counter += part.flat.notesAndRests[n].duration.quarterLength
                else:
                    length_counter = part.flat.notesAndRests[n].duration.quarterLength
                section_length.append(length_counter)
                section_type.append(part.flat.notesAndRests[n].isRest)

            else:
               length_counter += part.flat.notesAndRests[n-1].duration.quarterLength
               section_length.append(length_counter)
               section_type.append(part.flat.notesAndRests[n-1].isRest)
               # reset length
               length_counter = 0
               #print(section_length, '\n', section_type)
    section_length_bars = []
    section_info = []
    rest_section_bars = []
    restorplay = []
    barsrop =[]
    for n in range(len(section_length)):
        bars = section_length[n]/quarter_in_bar
        section_length_bars.append(bars)
        if section_type[n] == True:
            string = '{} bars of rest, '.format(bars)
            section_info.append(string)
            rest_section_bars.append(bars)
            barsrop.append(bars)
            restorplay.append('Rest')


        else:
            string = '{} bars of play, '.format(bars)
            section_info.append(string)
            barsrop.append(bars)
            restorplay.append('Play')

    print(section_info)
    if len(rest_section_bars) > 0:
        maximumRest = max(rest_section_bars)
    else:
        maximumRest = 0
    print('longest rest is', int(maximumRest), 'bars')

    dfrest = pd.DataFrame(
        {
            "Time Signature": [time_sig],
            "Total No. Bars": [bars_total],
            "No. Bars Rest": [bars_rest],
            "No. Bars Play": [bars_play],
            "Percentage of bars that are rest": [percentage_rest],
            "Longest Section of Rest": [maximumRest]
        }
    )
    dfsections = pd.DataFrame(
        {
            "Section Type": restorplay,
            "No. Bars of Section Type":barsrop,
        }
    )
    dfRest = pd.concat([dfrest,dfsections],axis=1)
    return dfRest, bars_total
