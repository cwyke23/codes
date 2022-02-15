# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 11:54:51 2020

@author: Cameron Wyke
"""



############################################################################################
################################## Libraries ###############################################
from pretty_midi import PrettyMIDI
import pandas as pd
from rounded_rectangle import rounded_rectangle
import cv2
import time
import os
from os import path
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from bar_detect import detect_bar
from whole_note_detection import detect_X
from tie_small import tie_check
from arrow import draw_arrow
from tie_same_page import tie_page
from key_sig  import scale_note
from sharp_detect_new import detect_sharp, real_note
import sys
from tempo_change import change_to_60


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
############################################################################################
############################################################################################



################################## User-Entry(Tentative) ###############################################


tempo = 60
midi_path = input("Enter the midi path: ")
midi_path = midi_path.replace("\\", "/")
#midi_path = "C:/Users/arvin/Documents/WeJam/Example Image Set/Living On A Prayer/LOAP.mid"
# midi_path = "C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/midi/26_3.mid"

input_directory_path = input("Enter the Input Directory: ")
input_directory_path = input_directory_path.replace("\\", "/") + '/'
#input_directory_path = "C:/Users/arvin/Documents/WeJam/Example Image Set/californication/Full res Musescore export/"
# input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/26_3/'
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/test_input/'
#input_directory_path = "C:/Users/arvin/Documents/WeJam/Example Image Set/Living On A Prayer/Uncoloured/"
#
#output_directory_path = input('Enter the directory where you would like to store the images: ')
#output_directory_path = output_directory_path.replace("\\", "/") + '/'

#output_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/test_Output/'

instrument = input("Enter the instrument: ")
instrument = instrument.lower()
# instrument = 'piano'

dir_path = input_directory_path + 'Coloured Notes'
if path.isdir(dir_path):
    pass
else:
    os.mkdir(dir_path)
output_directory_path = dir_path + '/'

time_signature = input("Enter the Time Signature: ")
# time_signature = int(time_signature)
# time_signature = '6/8'
time_sig = time_signature.split('/')
beats_per_bar = int(time_sig[0])
beat_note = int(time_sig[1])

key = input('Enter the key: ')


#flat_scale = input("Is the key in flat (Yes or No)?: ")
#flat_scale = flat_scale.lower()
bass = False
# key = 'D Major'
if instrument.lower() == "bass" :
    bass = True

###########################################################################################################
###########################################################################################################


################################## Static ###############################################
################################## Static ###############################################
colour = []
start_time = time.time() # Start timer after the user entered all the inputs
tempo = int(tempo)
change_to_60(midi_path)
pm = PrettyMIDI(midi_path)
df = pd.DataFrame()
bps = (tempo/60) * (beat_note/4)
font = ImageFont.truetype("fonts/Nootype - Radikal.otf", 80)



note_len_dict = {'Whole': 1, 'Partial Minim': 0.25, 'Quarter' : 0.25, 'Minim' : 0.25}


#start_df['Length'] = start_df['Type'].replace(note_len_dict)

tie_list = [2, 3/2, 1, 1/2, 1/4, 1/8, 1/16, 1/32]
for i in range(len(tie_list)):
    tie_list.append(tie_list[i]*1.5)
tie_list = sorted(tie_list)

beats_per_sec = float(tempo/60) * (beat_note/4)

# number of secs for a beat
sec_per_beat = 1/beats_per_sec

quarter_note = sec_per_beat * beat_note

# one bar in secs/
bar_sec = beats_per_bar * sec_per_beat

##########################################################################################
##########################################################################################
bar_array = pm.get_downbeats().tolist()
bar_sec_check = bar_array[1] - bar_array[0]

if (bar_sec - bar_sec_check) > 0.01:
    raise ValueError('Gotcha!!!!\nThe BPM is not 60. Request you to change it.')



bar_array.append(bar_array[-1] + bar_sec)
def bar(val):
    for i in range(0,len(bar_array)-1):
        now = bar_array[i]
        later = bar_array[i+1]
        if val >= now and val<later:
            return (i+1)
        else:
            pass

coord = detect_bar(input_directory_path)
start_dict= detect_X(input_directory_path)

# make a dataframe with Note, Start, End, Page, Bar
i = 0
df["Pitch"] = 0
df["Start"] = pm.get_onsets()
df["End"] = pm.get_end_time()
df["Page"] = 0
df['Bar'] = 0
df['Bar_start'] = 0

df['Duration'] = 0.0
df['whole'] = 'No'
tie_flag = False

#fill the dataframe with required info
for instrument_id in pm.instruments:
    count = 0
#    #print("instrument:", instrument_id.program)
    for note in instrument_id.notes:
#        if note.start > 50:
#            print(note.start)
        start = round(note.start,4)
        barr = bar(start)
        df['Bar'][i] = barr
        if barr == 0 or barr == 1:
            page = 1
        else:
            try:page = int((barr+1)/2)
            except:page = page
        df["Page"][i] = page
        df["End"][i] = note.end
        df["Pitch"][i] = note.pitch
        duration_fract = abs(note.end - note.start)/quarter_note
        df['Duration'][i] = round(duration_fract, 5)
        dur = df['Duration'][i]
        try: df['Bar_start'][i] = (barr-1)%2 + 1
        except: df['Bar_start'][i] = (bar(df['Bar'][i-1])-1)%2 + 1


        for j in range(len(tie_list)):
            probe = (tie_list[j] - dur)/dur
            if probe > 0.05 and probe < 0.1:
                dur = tie_list[j]
                tie_flag = False
                break
            else:
                tie_flag = True
        df['Duration'][i] = dur
        starting = int(note.start)
        bar_start = int(((df['Bar'][i]-1) *  beats_per_bar)/beats_per_sec)
        if starting == bar_start or starting == bar_start + 1:
            if df['Duration'][i] >= 0.92 and df['Duration'][i] <= 1.05 :
                df['whole'][i] = 'Yes'
                df['Duration'][i] = 1
#        df['Duration'][i] = dur

        i += 1
pos = 0


df_new = df
df_new['Tie'] = 'No'
df_new['Draw'] = False
div_bar = (32/beat_note) * beats_per_bar * (beat_note/4)


tie_count = 0
for k in range(len(df)):
    dur = df['Duration'][k]
    page = df['Page'][k]
    bar = df['Bar'][k]
#    if int(bar) == 29:
#        print('29')
    bar_start = ((df['Bar'][k]-1) *  beats_per_bar)/beats_per_sec
    div = bar_sec/div_bar
    start_div = abs(df['Start'][k]- bar_start)/bar_sec
    start_div = round( start_div  * div_bar)
    if start_div == div_bar:
        start_div = 0
    duration = round(dur * 32) * (beat_note/4)
    try:
        count += 1

        try:

            first, second, tie, bar_diff, three = tie_check(start_div, duration, time_signature)
#            print('\nPage: {}, Start_div: {} duration: {}\n first: {}, second: {}, tie: {}, bar_diff: {}, three: {}'.format(page, start_div, duration, first, second, tie, bar_diff, three))
        except:
            try:
                first, second, third, tie, bar_diff, three = tie_check(start_div, duration, time_signature)
                print('\nPage: {}, Start_div: {} duration: {}\n first: {}, second: {}, third: {} tie: {}, bar_diff: {}, three: {}'.format(page, start_div, duration, first, second, third, tie, bar_diff, three))
            except:
                pass
        if tie == True and three != True:

            tie_count += 1
            beat_diff = (beat_note/4)

            start_add = df['Start'][k] + (first/(32*beat_diff)) * 4 * beat_diff * sec_per_beat
            end_add = (start_add +  (first/(32*beat_diff)) * 4 * beat_diff * sec_per_beat) - 0.11
            df['End'][k] = start_add - 0.11
            df_new['Duration'][k] = first/(32 * beat_diff)
            duration_add = second/(32 * beat_diff)
            if duration_add > 0.92 and duration_add < 1.05:
                duration_add = 1
            bar_add = df['Bar'][k] + 1
            bar_start_add = (bar_add-1) % 2 + 1
            df_new['Tie'][k] = 'Yes'


            if bar_add % 2 == 0:
                pitch_add = 0
                page_add = df['Page'][k]
            else:
                pitch_add = df['Pitch'][k]
                page_add = df['Page'][k] + 1
            df_new = df_new.append({'Pitch':pitch_add,'Start': start_add, 'End': end_add, 'Page': page_add, 'Bar': bar_add, 'Bar_start': bar_start_add, 'Duration': duration_add, 'whole': 'No', 'Tie': 'Yes'}, ignore_index = True)

#            print('\n Page: {}, Bar: {}, Start: {}, Duration:{}, First: {}, Second: {}, Tie: {}, Bar Diff: {}'.format(page, bar, start_div, duration, first, second, tie, bar_diff))
        elif tie == True and three == True:
            notes = [first, second, third]
            beat_diff = (beat_note/4)
            df_new['Duration'][k] = first/(32*beat_diff)
            start_prev = df['Start'][k] + (first/32*beat_diff) * bar_sec
            bar_prev = df['Bar'][k]
            page_prev = df['Page'][k]
            for i in range(2):
                tie_count += 1
                first = notes[i]
                second = notes[i+1]
                start_add = start_prev + (first/div_bar) * bar_sec
                start_prev = start_add
                end_add = start_add + (second/div_bar) * bar_sec - 0.11
                df['End'][k] = start_add - 0.11

                duration_add = second/32
                bar_add = bar_prev + 1
                bar_prev = bar_add
                bar_start_add = (bar_add-1) % 2 + 1
                df_new['Tie'][k] = 'Yes'
                if i == 0:
                    draw = True
                else:
                    draw = False


                if bar_add % 2 == 0:
                    pitch_add = 0
                    page_add = page_prev

                else:
                    pitch_add = df['Pitch'][k]
                    page_add = page_prev + 1
                page_prev = page_add
                df_new = df_new.append({'Pitch':pitch_add,'Start': start_add, 'End': end_add, 'Page': page_add, 'Bar': bar_add, 'Bar_start': bar_start_add, 'Duration': duration_add, 'whole': 'No', 'Tie': 'Yes', 'Draw': draw}, ignore_index = True)

    except:
        pass
    #                elif k == len(df_funct)-1:
    #                    df_funct['Pos'][k] = pos
df_new = df_new.sort_values(by=['Page', 'Start'])
df_new = df_new.reset_index(drop = True)





j = 24

notes = ['C','C#','D','D#', 'E', 'F','F#', 'G', 'G#', 'A','A#','B']
note_dict = {0:'', 21: 'A_0', 22: 'A#_0', 23: 'B_0', 108: "C_8"}
for i in range (1,8):
    for note in notes:
        note = note + "_" + str(i)
        note_dict[j] = note
        j += 1

###########################################################################
key_notes = scale_note(key)
sharp_df = detect_sharp(input_directory_path, bass)

###########################################################################

#########################################################################################################################################
######################################## Colouring Function #############################################################################
#########################################################################################################################################

def colour_image(img, page, colour):
    #print('\nThe image path is: {}\n'.format(path_image))
    pos = 0

    # Time Signature



    #beats/min
    bpm = tempo

    #number of beats in a sec
    beats_per_sec = float(bpm/60)


    # One division
    div = (beats_per_bar/(beat_note/4))/div_bar


    page_list = df_new.index[df_new['Page']==page].tolist()
    df_funct = pd.DataFrame()
    df_funct['Pitch'] = 0
    df_funct['Bar'] = 0
    df_funct['Start'] = 0
    df_funct['End'] = 0


    df_funct = df_new.iloc[page_list, :]
    df_funct['Pos'] = 0
    df_funct['Whole'] = 'False'
    df_funct['Same Bar'] = 'No'
    df_funct = df_funct.sort_values(by=['Start', 'Pitch'])
    df_funct = df_funct.reset_index(drop = True)


    for k in range(len(df_funct)):

        stack_tie = False
        page = page
#        if page == 15:
#            print('20')
        bar = df_funct['Bar_start'][k]
        start=  df_funct['Start'][k]
        end = df_funct['End'][k]
        bar_number = ((page - 1) * 2) + bar -1
        start_bar = bar_number * bar_sec
        start_time = start-start_bar
        start_div = int(round((start_time/bar_sec)*(16*(beats_per_bar/beat_note)))) + 1
        dur = df_funct['Duration'][k]
        if dur >= 0.51 and dur < 0.55 and dur != 0.5:
            dur = 0.5625
        if dur >= 0.39 and dur < 0.43 and dur != 0.3125:
            dur = 0.4375
        if dur > 0.3 and dur < 0.3125:
            dur = 0.3125
        if dur >= 0.63 and dur < 0.6875  :
            dur = 0.6875
        if dur > 0.76 and dur <= 0.825:
            dur = 0.8125
        if dur > 0.828 and dur < 0.88:
            dur = 0.875
        if dur >= 0.88 and dur <= 0.96:
            dur = 0.94
        if (dur*16) - round(dur*16,0)>=0.45:
            duration_tie = round(dur*16,0) + 1
        else:
            duration_tie = round(dur*16,0)
        start_tie = start_div
        tie = tie_page(beats_per_bar, start_tie, duration_tie)
        if k < len(df_funct)-1 and df_funct['Start'][k] ==  df_funct['Start'][k+1]:
            df_funct['Pos'][k] = pos
        elif k > 0 and df_funct['Start'][k] ==  df_funct['Start'][k-1] and df_funct['Same Bar'][k-1] == 'Yes':
            df_funct['Pos'][k] =  df_funct['Pos'][k-1]
            pos += 1
            stack_tie = True


#                elif k == len(df_funct)-1:
#                    df_funct['Pos'][k] = pos
        else:
            df_funct['Pos'][k] = pos
            pos +=1
        if tie != False:
            print("Page:{}, Duration: {}, Start: {}".format(page, duration_tie, start_tie))
            df_funct['Duration'][k] = df_funct['Duration'][k] + 0.5*tie
            df_funct['Same Bar'][k] = 'Yes'
            if stack_tie != True:
                pos += tie
            if k < len(df_funct)-1 and df_funct['Bar'][k+1] !=  df_funct['Bar'][k]:
               df_funct['Duration'][k] = df_funct['Duration'][k] + 3*tie

    start_prev = 0
    height_offset = 0
    bar_prev = 0
    cv2_im_processed = img
    for i in range(len(df_funct)):
        img = cv2.imread(filename)
        pitch = df_funct['Pitch'][i]
        page = page
        bar = df_funct['Bar_start'][i]
        start=  df_funct['Start'][i]
        end = df_funct['End'][i]
        change = False

        # check for multiple notes
        if start_prev == start:
            height_offset+=1
            start_prev = start
        else:
            start_prev = start
            height_offset = 0
        #
        if bar_prev == bar:
            pass
        else:
            height_offset = 0
            bar_prev = bar

        note = note_dict[pitch].split("_")[0]

        bar_number = ((page - 1) * 2) + bar -1
        #    start = 105
        #    end = 107.186

        start_bar = (bar_number * beats_per_bar)/beats_per_sec

        start_time = start-start_bar
#                #print('The start time is {}'.format(start_time))
        end_time = end - start_bar

        start_div = int(round(start_time/div))
        end_div = round(end_time)/div
        end_div = int(round(end_div))
#                #print('rounded end div: ' + str(end_div))
        if df_funct['Tie'][i] == 'Yes':
            div_diff = df_funct['Duration'][i] * div_bar
        else:
            div_diff = abs(end_div - start_div)
        if div_diff >= div_bar/(0.5 * beats_per_bar) and div_diff != div_bar:
            div_diff -= 1
        div_diff -= 2
        if div_diff < 6:
                div_diff = 5
        try:
            middle = coord['Middle'][page-1]
        except:
            break
        end_bar2 = coord['End'][page-1]
        mid = middle - 4
        inc_ratio  = mid/1010
        start_x = 180 * inc_ratio
        last_point = (inc_ratio * 980)
        beat_div = (last_point - start_x)/(div_bar/(beat_note/4))
        if page == 30:
            pass
        if bar == 1:

            pos = df_funct['Pos'][i]
            #print('\nThis is BAR 1!')

#                    middle = coord['Middle'][page-1]
#                    mid = middle - 4
#                    inc_ratio  = mid/1000
#                    start_x = 180 * inc_ratio
#                    last_point = (inc_ratio * 980)
#            last_point = last_point - (last_point % 32)


            if df_funct['whole'][i] == 'Yes' and df_funct['Whole'][i] == 'True':

                start_list = list(start_dict[page].keys())
                try:

                    start_pos = start_list[pos]
#                    print('Bar2! Page:{}, Start_whole: {}'.format(page, start_pos))
                except:
                    pass
                x1 = int(round(start_pos)) -35

            else:
                pass



            if len(start_dict[page]) != 0:
                try:
                    start_list = list(start_dict[page].keys())
                    start_pos = start_list[pos]
                    x1 = int(round(start_pos)) -25
                except:
                    print('Pos: {}, Page: {}'.format(pos, page))
            end_offset = df_funct['Duration'][i]* 32 * beat_div
            if end_offset <= 95:
                end_offset = 95
            try:
                x2 = int(x1 + end_offset) - 20
            except:
                pass
            try:
                k = i
                try:
                    while (df_funct['Pos'][i] == df_funct['Pos'][k+1]) and k < len(df_funct)-1:
                        k += 1
                except:
                    pass
                if df_funct['Same Bar'][i] == 'Yes':
                        try:
                            tie_pos = df_funct['Pos'][k+1] - 1
                        except:
                            tie_pos = len(start_list) -1
                        try:
                            x2 = start_list[tie_pos] + 30
                        except:
                            pass
                if x2 > last_point - 10:

                    x2 = int(round(last_point - 10))
                try:
                    pos_check = df_funct['Pos'][k+1]
                    x_check = int(round(start_list[pos_check]))
                    if (x_check - x2) < 40  and pos != pos_check:
                        x2 = x_check - 55
#                    if df_funct['Same Bar'][i] == 'Yes':
#                        try:
#                            tie_pos = df_funct['Pos'][k+1] - 1
#                        except:
#                            tie_pos = len(start_list) -1
#                        try:
#                            x2 = start_list[tie_pos] + 30
#                        except:
#                            pass
                except:
                    pass
            except:
                print('Check here mate!')
            try:
                if df_funct['Pitch'][k+1] == 0:
                    x2 = x2 + 70
            except:
                pass

            #print('\nX1_bar2:' + str(x1))
            #print('X2_bar2: ' + str(x2))
            #print('The Beat_division is:' + str(beat_div))
            #print('The first bar starts from:' + str(start_x))
            #print('The length of the note is:{} divisions'.format(div_diff))
            #print('The different in length, pixel wise is: {}'.format(x2-x1))

        elif bar == 2:
            #print('\nThis is BAR 2!')
            pos = df_funct['Pos'][i]
            start_x = middle + (0.04 * (1852-middle))
            if df_funct['whole'][i] == 'Yes' or df_funct['Whole'][i] == 'True':

#                        beat_div = (1852 - start_x)/32

                start_list = list(start_dict[page].keys())
                try:
                    start_pos = start_list[pos]
#                    print('Bar2! Page:{}, Start_whole: {}'.format(page, start_pos))
                except:
                    pass
                x1 = int(round(start_pos)) -35
            elif df_funct['Tie'][i] == 'Yes' and df_funct['Pitch'][i] == 0:
                if height_offset > 0:
                    x1 = x1_prev
                    x2 = x2_prev
                    change = True
                else:
                    x1 = x2_prev - 50
                    change = True
                    if abs(x1 - x1_prev) <= 40:
                        x1 = x1 + 20
                colour = colour_list[height_offset]
                pos = df_funct['Pos'][i]

                div_diff +=4
#                    elif df_funct['Same Bar'][i] == 'Yes':
#                        x1 = x2_prev - 40
#                        div_diff +=3
            else:
                pass
                pos = df_funct['Pos'][i]
                if len(start_dict[page]) != 0:
                    try:
                        start_list = list(start_dict[page].keys())
                        start_pos = start_list[pos]
                        x1 = int(round(start_pos)) -35
                    except:
                        print('Page: {}, pos: {}'.format(page, pos))
            end_offset = df_funct['Duration'][i]* 32 * beat_div
            if end_offset <= 95:
                end_offset = 95
            if change == True:
                end_offset += 90
                try:
                    x2 = int(start_list[df_funct['Pos'][i]] + end_offset) - 80
                except:
                    pass
            else:
                x2 = int(x1 + end_offset) - 20
            y =180 - height_offset*60
            start_list = list(start_dict[page].keys())
            if df_funct['Same Bar'][i] == 'Yes':
                try:
                    tie_pos = df_funct['Pos'][i+1] - 1
                except:
                    tie_pos = len(start_list) -1
                x2 = start_list[tie_pos] + 30


            if x2 > end_bar2 - 10:
                x2 = int(round(end_bar2 - 10))
            if (df_funct['Tie'][i] == 'Yes' and df_funct['Pitch'][i] != 0) or df_funct['Draw'][i]==True:
                x2 = int(end_bar2 - 20)
                pos = (x2,y)
                img = draw_arrow(filename,pos)
            try:
                k = i
                while df_funct['Pos'][k] == df_funct['Pos'][k+1] and k<len(df_funct)-1:
                    k +=1
                pos_check = df_funct['Pos'][k+1]
                x_check = int(round(start_list[pos_check]))
                if (x_check - x2) < 40  and pos != pos_check:
                    x2 = x_check - 55
            except:
                pass

            #print('\nX1_bar2:' + str(x1))
            #print('X2_bar2: ' + str(x2))
            #print('The Beat_division is:' + str(beat_div))

            #print('The Second bar starts from:' + str(start_x))
            #print('The length of the note is:{} divisions'.format(div_diff))
            #print('The different in length, pixel wise is: {}'.format(x2-x1))

        else:
            print("Error!")
        #        break




        if page== 78:
            pass

        y =180 - height_offset*60
        try:

            top_left = (x1,y)
        except:
            pass
        try:
            bottom_right = (x2, y+50)
        except:
            pass
        x2_prev = x2
        x1_prev = x1

        #######################################################
        ## check for accidental -- START! ##
        #######################################################

        flat = True
        y_temp = []
        if note in key_notes:
            flat = False

        else:
#                    try:
            pos = df_funct['Pos'][i]
            page_list = sharp_df.index[sharp_df['Page']==page].tolist()
            df_temp = sharp_df.iloc[page_list, :]
            df_temp = df_temp.reset_index(drop = True)
            for i in range(len(df_temp)):
                for j in range(len(start_list)):
                    if abs(df_temp['Start'][i] - start_list[j])< 45:
                        df_temp['X_Pos'][i] = j



            pos_list = df_temp.index[df_temp['X_Pos']==pos].tolist()
            df_temp = df_temp.iloc[pos_list, :]
            df_temp = df_temp.reset_index(drop = True)
            df_temp['Y_Pos'] = 0
            df_temp = df_temp.sort_values(by=['Height'], ascending = False)
            df_temp = df_temp.reset_index(drop = True)
            try:
                start_pos = start_list[pos]
            except:
                pass
            temp_list = start_dict[page][start_pos]

            k = 0
            for k in range(len(df_temp)):
                for i in range(len(temp_list)):
                    height = df_temp['Height'][k]
                    if abs(height - temp_list[i]) < 5:
                        df_temp['Y_Pos'][k] = i


            try:
                y_temp = df_temp.index[df_temp['Y_Pos']==height_offset].to_list()[0]
                if note == df_temp['Note'][y_temp]:
                    note = df_temp['Note'][y_temp]
                    flat = False

            except:
                pass

        if flat == True:
            note = real_note(note)

        #######################################################
        ## check for accidental -- FINISH! ##
        #######################################################

        ## The colours below are in BGR and not RGB
        magenta = (155, 0, 255)
        cyan = (245, 200, 0)
        yellow = (15 , 230, 255)
        green = (70, 195, 20)
        orange = (25,155,255)

        #bass
        if instrument == "bass" or instrument == "Bass":
            if (pitch > 20 and pitch < 32) or (pitch == 32 and flat == False) or (pitch == 20 and flat == True):
                colour = magenta
            elif pitch > 32 and pitch < 44 or (pitch == 44 and flat == False) or (pitch == 32 and flat == True):
                colour = cyan
            elif pitch > 44 and pitch < 56 or (pitch == 56 and flat == False) or (pitch == 44 and flat == True):
                colour = yellow
            elif pitch > 56 and pitch < 68 or (pitch == 68 and flat == False) or (pitch == 56 and flat == True):
                colour = green

        # piano
        elif instrument == "piano" or instrument == "Piano":
            if pitch > 20 and pitch < 32 or (pitch == 32 and flat == False) or (pitch == 20 and flat == True):
                colour = magenta
            elif pitch > 32 and pitch < 44 or (pitch == 44 and flat == False) or (pitch == 32 and flat == True):
                colour = magenta
            elif pitch > 44 and pitch < 56 or (pitch == 56 and flat == False) or (pitch == 44 and flat == True):
                colour = cyan
            elif pitch > 56 and pitch < 68 or (pitch == 68 and flat == False) or (pitch == 56 and flat == True):
                colour = yellow
            elif pitch > 68 and pitch < 80 or (pitch == 80 and flat == False) or (pitch == 68 and flat == True):
                colour = green
            elif pitch > 80 and pitch < 92 or (pitch == 92 and flat == False) or (pitch == 80 and flat == True):
                colour = orange

                # guitar
        elif instrument.lower() == "guitar":
            if pitch > 44 and pitch < 56 or (pitch == 56 and flat == False) or (pitch == 44 and flat == True):
                colour = magenta
            elif pitch > 56 and pitch < 68 or (pitch == 68 and flat == False) or (pitch == 56 and flat == True):
                colour = cyan
            elif pitch > 68 and pitch < 80 or (pitch == 80 and flat == False) or (pitch == 68 and flat == True):
                colour = yellow
            elif pitch > 80 and pitch < 92 or (pitch == 92 and flat == False) or (pitch == 80 and flat == True):
                colour = green
        else:
            print("Sorry! {} is not available yet".format(instrument.capitalize))
        # font
        font = ImageFont.truetype("fonts/Nootype - Radikal.otf", 40)
        try:
            if height_offset == 0  and df_funct['Pitch'][i] != 0:
                colour_list = []
                colour_list.append(colour)
            elif df_funct['Pitch'][i] == 0:
                pass
            else:
                colour_list.append(colour)
        except:
            print('failed')
        # img = np.zeros(image_size)
        try:
            img = rounded_rectangle(img, top_left, bottom_right, color=colour, radius=2, thickness=-1)
            if height_offset == 0 and df_funct['Pitch'][i] != 0:
                colour_list = []
                colour_list.append(colour)
            elif df_funct['Pitch'][i] == 0:
                pass
            else:
                colour_list.append(colour)
        except:
            colour_prev = colour_list[height_offset]
            print('top_left: {}, bottom_right: {}, page:{}, colour: {},\nimg: {}'.format(top_left, bottom_right, page, img, colour_prev))
        cv2.imwrite(filename, img)
        # Using cv2.putText() method
        img = cv2.imread(filename)


        # Convert the image to RGB (OpenCV uses BGR)
        cv2_im_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        # Pass the image to PIL
        pil_im = Image.fromarray(cv2_im_rgb)

        draw = ImageDraw.Draw(pil_im)


        if note.endswith('\u266D'):
            word = note.split(' ')
            draw.text((top_left[0]+15, top_left[1]+10), word[0], (0, 0, 0), font=font)
            word_size = font.font.getsize(word[0])
            font  = ImageFont.truetype("fonts/Musisync-KVLZ.ttf", 70)
            draw.text((top_left[0]+20 + word_size[0][0], top_left[1]-50), 'b', (0, 0, 0), font=font)

        else:
            draw.text((top_left[0]+15, top_left[1]+10), note, (0, 0, 0), font=font)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
#                cv2.imshow('PIL_image', cv2_im_processed)
#                cv2.waitKey(0)
        cv2.imwrite(filename, cv2_im_processed)

    try:
        return cv2_im_processed, colour_list
    except:
        return cv2_im_processed, colour
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

# Image processing starts here

for path_image in os.listdir(input_directory_path):
    if path_image.endswith(".png"):
        print('\n',path_image)

        input_path = input_directory_path + path_image
        try:

            page = int(path_image.split('-')[-1].split(".")[0])
        except:
            page = int(path_image.split(' ')[-1].split(".")[0])
        pos = 0


        im = cv2.imread(input_path, -1) # keep alpha
        im = cv2.resize(im, (1920, 600))
        alpha = im[:,:,3] # extract it
        binary = ~alpha

        filename = 'temp.jpg'
        #
        ## Using cv2.imwrite() method
        # Saving the image
        cv2.imwrite(filename, binary)
#        img = cv2.imread(filename)

        img = cv2.imread(filename)
        ## Using cv2.imwrite() method
        ## Saving the image
        cv2.imwrite(filename, binary)
        cv2_im_processed = img
        start_prev = 0
        temp, colour = colour_image(img, page, colour)
    else:
        pass
    output_path = output_directory_path + path_image.split('.')[0] + '.png'
    try:
        cv2.imwrite(output_path,temp )
    except:
        print('Not an error!! {} cannot be processed'.format(path_image))
stop = time.time()
print('Time taken to run this program was: {}'.format(stop-start_time))
#        temp_img = cv2.imread(output_path)
#        cv2.imshow(output_path, temp_img)
#        cv2.waitKey(0)
