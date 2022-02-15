# -*- coding: utf-8 -*-
"""
Created on Feb 22 2021
Code to process Rhythm Information from xml part
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
 #number of notes of each length
    #part.show('text')
def rhythm_analysis(part,instrument,level):
    piece_note_values = []
    #quarter length for no crotchets, duration.type for names
    for n in part.flat.notes:
         #print(n.pitch.name, n.pitch.octave, n.duration.type)
        if n.quarterLength not in piece_note_values:
             piece_note_values.append(n.quarterLength)
        #print(piece_note_values)
        #define function to return zeros vector of same length as input
    def zeros(piece_note_values):
        blank_list = []
        for i in range(len(piece_note_values)):
            blank_list.append(0)
        return blank_list

    duration_counter = zeros(piece_note_values)
    beat_strength_full = zeros(piece_note_values)
    beat_strength_half = zeros(piece_note_values)
    beat_strength_quarter = zeros(piece_note_values)
    notes = part.flat.notes
    for i in range(len(piece_note_values)):
        for n in part.flat.notes:
            if n.quarterLength == piece_note_values[i]:
                duration_counter[i] += 1
                #print(n.beatStrength)
                if n.beatStrength == 1:
                    beat_strength_full[i] += 1
                elif n.beatStrength == 0.5:
                    beat_strength_half[i] += 1
                elif n.beatStrength == 0.25:
                    beat_strength_quarter[i] += 1

    #print(duration_counter)
    print('There are {} notes in total'.format(len(part.flat.notes)))
    no_note_durations = len(piece_note_values)
    piece_note_values_names = []
    #quarter length for no crotchets, duration.type for names
    for n in part.flat.notes:
        #print(n.pitch.name, n.pitch.octave, n.duration.type)
        if n.duration.type not in piece_note_values_names:
            piece_note_values_names.append(n.duration.type)
    print('There are {} note values:'.format(no_note_durations))
    for i in range(len(piece_note_values_names)):
        print(piece_note_values_names[i])
    for i in range(len(piece_note_values)):
        print( duration_counter[i], ' instances of notes ', piece_note_values[i], ' quarter length')
        print ('of which : {} first beat, {} weaker beats, {} offbeats'.format(beat_strength_full[i], beat_strength_half[i], beat_strength_quarter[i]))
    average_note_value = 0
    #average note length
    for l in range(len(duration_counter)):
        average_note_value += duration_counter[l]*piece_note_values[l]

    average_note_value = average_note_value/len(part.flat.notes)


    #Percentage of notes on strong, middle ,weak beat
    strong_sum = 0
    middle_sum = 0
    weak_sum = 0
    for n in range(len(beat_strength_full)):
        strong_sum += beat_strength_full[n]
        middle_sum += beat_strength_half[n]
        weak_sum += beat_strength_quarter[n]
    strong_perc = (strong_sum/len(part.flat.notes))*100
    middle_perc = (middle_sum/len(part.flat.notes))*100
    weak_perc = (weak_sum/len(part.flat.notes))*100



    df1 = pd.DataFrame(
        {
        "Instrument":[instrument],
        "Level":[level],
        "No. of Notes": [len(part.flat.notes)],
        "No. Different Note Values": [no_note_durations]
        }
    )
    df2 = pd.DataFrame(
        {
              "Used Lengths (in quarter length)": piece_note_values,

              "No. of Notes of Length": duration_counter,

              "No. of Notes on First Beat" : beat_strength_full,

              "No. of Notes on Weaker Beats" : beat_strength_half,

              "No. of Notes on Off Beat" : beat_strength_quarter

        }
    )
    df3 = pd.DataFrame(
        {
            "Total Lengths Used": [len(piece_note_values)],
            "Average Note Length": [average_note_value],
            "Percentage of Notes on First Beat" : [strong_perc],
            "Percentage of Notes on Weaker Beats" : [middle_perc],
            "Percentage of Notes on Off Beat" : [weak_perc]
        }
    )

    dfrhythm = pd.concat([df1,df2,df3],axis=1)
    return dfrhythm, piece_note_values
