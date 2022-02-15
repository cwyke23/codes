# -*- coding: utf-8 -*-
"""
Created on Feb 22 2021
Code to process Pitch Information from xml part
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
def pitch_analysis(part,piece_note_values):

    print('PITCH')
    accidental_count = 0
    natural_count = 0
    no_chords=0
    full_pitches_w_chords = []
    full_durations_w_chords = []
    for n in part.flat.notes:
        if len(n.pitches) > 1:
            no_chords += 1
        for p in n.pitches:
            full_pitches_w_chords.append(p)
            full_durations_w_chords.append(n.quarterLength)
            if '#' in p.name or '-' in p.name:
                accidental_count += 1
            else:
                natural_count += 1
    print('{} naturals and {} accidentals'.format(natural_count, accidental_count))

# no. of pitches, durations and duration pitch combos
    no_durations = len(piece_note_values)

    no_pitches_octaves = []
    for n in full_pitches_w_chords:
            #print((n.pitch.name))

            if n.nameWithOctave not in no_pitches_octaves:
                no_pitches_octaves.append(n.nameWithOctave)
    no_pitches_octaves.sort()
    #print(no_pitches_octaves)
    no_pitches_overall = len(no_pitches_octaves)

#print number occurences of each pitch
    pitches = [['A'],['A#','Bb'],['B','Cb'],['B#','C'],['C#','Db'],['D'],['D#','Eb'],['E','Fb'],['E#','F'],['F#','Gb'],['G'],['G#','Ab']]
    pitch_counter = 0
    pitch_counter_array = []

#without octaves
    for p in pitches:
        for n in full_pitches_w_chords:
            #print((n.pitch.name))

            if n.name in p:
                pitch_counter += 1
        pitch_counter_array.append(pitch_counter)
        pitch_counter = 0

    #for p in range(len(pitches)):
        #print('{} {}s \n'.format(pitch_counter_array[p],pitches[p]))

    pitch_counter_array_2 =[]
    #with octaves
    for p in no_pitches_octaves:
        for n in full_pitches_w_chords:
            #print((n.pitch.name))

            if n.nameWithOctave == p:
                pitch_counter += 1
        pitch_counter_array_2.append(pitch_counter)
        pitch_counter = 0

    #for p in range(len(no_pitches_octaves)):
       # print('{} {}s \n'.format(pitch_counter_array_2[p],no_pitches_octaves[p]))
    # no of octaves used:
    octaves = []
    for p in no_pitches_octaves:
        if p[-1] not in octaves:
            octaves.append(p[-1])
    print('the piece uses {} pitches from {} octaves'.format(len(no_pitches_octaves),len(octaves)))


#Key
    keys= part.flat.getKeySignatures()
    key_sig = str(keys.keySignature)
    key_sig = key_sig[29:-1]


    dfpitch = pd.DataFrame(
        {
            "Key Signature":[key_sig],
            "No. Naturals":[natural_count],
            "No. Accidentals":[accidental_count],
            "No. Chords":[no_chords],
            "Total No. of Pitches Used":[len(no_pitches_octaves)],
            "No. of Octaves Used":[len(octaves)],
        }
    )
    # splitting pitches down into pitches w octaves
    small_list =[]
    full_pitch_list = []
    small_list_pitch =[]
    full_count_list = []
    for p in pitches:
        for n in range(len(no_pitches_octaves)):
            pitch_octave = no_pitches_octaves[n]
            #print(pitch_octave[:-1])
            if any(pitch == pitch_octave[:-1] for pitch in p):
                small_list.append(pitch_counter_array_2[n])
                small_list_pitch.append(pitch_octave)
                #print(pitch_octave)
        other = small_list[:]
        other_pitch = small_list_pitch[:]
        full_pitch_list.append(other_pitch)
        full_count_list.append(other)
        small_list = []
        small_list_pitch = []
    #print(full_pitch_list, '\n', full_count_list)
    #printing
    pitcheswoctaves = []
    pitcheswoctavescount = []
    for p in range(len(full_count_list)):
        full_count_small = full_count_list[p]
        full_pitch_small = full_pitch_list[p]

        print(' {} {}s in which there are:'.format(pitch_counter_array[p], pitches[p]))
        for pitch in range(len(full_count_small)):
             pitcheswoctavescount.append(full_count_small[pitch])
             pitcheswoctaves.append(full_pitch_small[pitch])
             print( '{} {}s'.format(full_count_small[pitch], full_pitch_small[pitch]))
    dfp = pd.DataFrame(
        {
            "Pitch":pitches,
            "No. Instances of Pitch":pitch_counter_array,
        }
    )
    dfpoct = pd.DataFrame(
        {
            "Pitch with Octave ": pitcheswoctaves,
            "No. Instances of Pitch":pitcheswoctavescount,
        }
    )

    #print number of occurences of each note length per pitch

    #for each pitch not octave
    duration_counter_array = [0,0,0,0] #counter array
    pitch_duration_counter = [] #array to put arrays in
    for p in pitches:

        #print(p)
        #print(duration_counter_array,'!!')
        #print(pitch_duration_counter)

        for n in range(len(full_pitches_w_chords)):

            #print('new note')
            #SEMIBREVE
            if full_durations_w_chords[n] == 4.0 and full_pitches_w_chords[n].name in p:
                    duration_counter_array[0] += 1
            #MINIM
            elif full_durations_w_chords[n] == 2.0 and full_pitches_w_chords[n].name in p:
                    duration_counter_array[1] += 1
            #CROTCHET
            elif full_durations_w_chords[n] == 1.0 and full_pitches_w_chords[n].name in p:
                    duration_counter_array[2] += 1
            #OTHER NOTE VALUE
            elif full_durations_w_chords[n] != 4.0 and full_durations_w_chords[n] != 2.0 and full_durations_w_chords[n] != 1.0 and full_pitches_w_chords[n].nameWithOctave == p:
                    duration_counter_array[3] += 1
            #for l in range(len(piece_note_values)):
                #if full_durations_w_chords[n] == piece_note_values[l] and full_pitches_w_chords[n].name in p:
                    #duration_counter_array[l] += 1
                    #print(duration_counter_array,n.quarterLength,n.pitch.name)

        pitch_duration_counter.append(duration_counter_array[:])
        duration_counter_array = [0,0,0,0]
        #for d in range(len(duration_counter_array)):
            #duration_counter_array[d] = 0


    #new naming to help with csv
    excel_values = ['Semibreve', 'Minim', 'Crotchet', 'Other']
    piece_note_values2 = []
    for i in range(len(excel_values)):
        string = "No. of pitch with " + str(excel_values[i]) + " Length"
        piece_note_values2.append(string)
    print(piece_note_values2)

    #print(pitch_duration_counter, '\n', pitch_counter_array)
    #for p in range(len(pitch_duration_counter)):
       # p_array = pitch_duration_counter[p]
        #for n in range(len(p_array)):
           # no_zeros = p_array.count(0)
            #if no_zeros != (len(p_array)):
              #  print('{} {}s of length {}'.format(p_array[n],pitches[p],piece_note_values[n]))
    test = {}
    for p in range(len(pitch_duration_counter)):
        p_array = pitch_duration_counter[p]

        for n in range(len(p_array)):
            if piece_note_values2[n] not in test:
                test[piece_note_values2[n]] = []

            test[piece_note_values2[n]].append(p_array[n])
    print(test)
    dfpc = pd.DataFrame(test)

    #for each pitch with octave

    duration_counter_array = [0,0,0,0] #counter array
    pitch_duration_counter_2 = [] #array to put arrays in
    for p in no_pitches_octaves:

        #print(p)
        #print(duration_counter_array,'!!')
        #print(pitch_duration_counter)

        for n in range(len(full_pitches_w_chords)):
            #print('new note')
            #SEMIBREVE
            if full_durations_w_chords[n] == 4.0 and full_pitches_w_chords[n].nameWithOctave == p:
                    duration_counter_array[0] += 1
            #MINIM
            elif full_durations_w_chords[n] == 2.0 and full_pitches_w_chords[n].nameWithOctave == p:
                    duration_counter_array[1] += 1
            #CROTCHET
            elif full_durations_w_chords[n] == 1.0 and full_pitches_w_chords[n].nameWithOctave == p:
                    duration_counter_array[2] += 1
            #OTHER
            elif full_durations_w_chords[n] != 4.0 and full_durations_w_chords[n] != 2.0 and full_durations_w_chords[n] != 1.0 and full_pitches_w_chords[n].nameWithOctave == p:
                    duration_counter_array[3] += 1
            #for l in range(len(piece_note_values)):
                #if full_durations_w_chords[n] == piece_note_values[l] and full_pitches_w_chords[n].nameWithOctave == p:
                    #duration_counter_array[l] += 1
                    #print(duration_counter_array,n.quarterLength,n.pitch.name)

        pitch_duration_counter_2.append(duration_counter_array[:])
        duration_counter_array = [0,0,0,0]
        #for d in range(len(duration_counter_array)):
            #duration_counter_array[d] = 0


    #print(pitch_duration_counter, '\n', pitch_counter_array)
    pitch_duration_combos = 0
    for p in range(len(pitch_duration_counter_2)):
        p_array = pitch_duration_counter_2[p]
        for n in range(len(p_array)):
            no_zeros = p_array.count(0)
            if no_zeros != (len(p_array)):
                print('{} {}s of length {}'.format(p_array[n],no_pitches_octaves[p],excel_values[n]))
                if p_array[n] != 0:
                    pitch_duration_combos += 1

    test2 = {}
    for p in range(len(pitch_duration_counter_2)):
        p_array = pitch_duration_counter_2[p]

        for n in range(len(p_array)):
            if piece_note_values2[n] not in test2:
                test2[piece_note_values2[n]] = []

            test2[piece_note_values2[n]].append(p_array[n])
    #print(test2)
    dfpcoct = pd.DataFrame(test2)


    print('There are {} different pitch and duration combos'.format(pitch_duration_combos))



    # print intervals:
    under_third = 0
    under_fifth = 0
    under_octave = 0
    over_octave = 0
    total_i = 0
    max_int = 0
    intList = analysis.segmentByRests.Segmenter.getIntervalList(part)
    #average_int = statistics.mean(intList)
    for i in intList:
        total_i = total_i + abs(i.semitones)
        #print(i.name)
        #print(i.niceName)
        if i.semitones <= 4:
            under_third += 1
        elif i.semitones >4 and i.semitones <= 7:
            under_fifth += 1
        elif i.semitones > 7 and i.semitones <= 12:
            under_octave += 1
        else:
             over_octave += 1
    #maximum interval
    for i in intList:
             if i.semitones > max_int:
                 max_int = i.semitones
    #average interval
    average_int = total_i/len(intList)
    print( '{} intervals under a third, {} intervals between third and fifth, {} intervals\
    between fifth and octave and {} intervals over an octave,\
           average interval {}, max interval {}'.format(under_third,under_fifth,under_octave,over_octave,average_int,max_int))
    dfint = pd.DataFrame(
        {
            "No. Pitch Duration Combos":[pitch_duration_combos],
            "Intervals Under Third":[under_third],
            "Intervals Between Third and Fifth":[under_fifth],
            "Intervals Between Fifth and Octave":[under_octave],
            "Intervals Over Octave":[over_octave],
            "Average Interval":[average_int],
            "Maximum Interval":[max_int],
        }
    )

    dfPitch = pd.concat([dfpitch,dfp,dfpc,dfpoct,dfpcoct,dfint], axis=1)
    return dfPitch
