# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:18:48 2021

@author: arvin
"""
import cv2
import pandas as pd
import os
from os import path
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
#####################################################################################
   ## Sharp sign image recognition function ##
#####################################################################################

def detect_sharp(input_directory_path, bass = False):
    
    start_x = []
    start_min, start_max = [], []
    page_number = []
    dir_path = input_directory_path + 'Sharp Detects'
    if path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)     
        
    for path_image in os.listdir(input_directory_path):
        
        if path_image.endswith(".png"):
            # print(path_image)
            
            input_path = input_directory_path + path_image
            try:
                page = int(path_image.split('-')[-1].split(".")[0])
            except:
                page = int(path_image.split(' ')[-1].split(".")[0])
#            print('\n', page)
        #        input_dir  ="C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/weirder/New Images 17th Dec-{}.png".format(i)
#             print('\n',image)
            img  = cv2.imread(input_path, -1)
            #image = cv2.imread(input_path, -1)
            #img = cv2.resize(img, (2525, 421))
            img = cv2.resize(img, (1920, 600))
            alpha = img[:,:,3] # extract it
            binary = ~alpha
            
            filename = 'temp.jpg'
            
            cv2.imwrite(filename, binary)
            img = cv2.imread(filename)
            
            
            # Hollow notes 
            blur=cv2.GaussianBlur(img,(19,15),0)
            gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            returns,thresh=cv2.threshold(gray,40,255,cv2.THRESH_BINARY)
            
            contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
            
                area=cv2.contourArea(cnt) #contour area
                
                edges = len(cnt)
                cnt = cnt.reshape(edges, 2)  
                min_x = min(cnt.transpose()[0])
                max_x = max(cnt.transpose()[0])
                avg_x = int((round(max_x + min_x))/2)
                length = max_x - min_x
                
                top_x = min(cnt.transpose()[1])
                bottom_x = max(cnt.transpose()[1])
                height = abs(top_x-bottom_x)
                avg_y = int((round(top_x + bottom_x))/2)
#                cv2.drawContours(img,[cnt],-1,(0, 0, 255),2)
#                print('Area: {}, Length: {}, Height: {} avg_x: {}'.format(area, length, height, avg_x))
        #        # print('min_x: ', min_x)
            #    if area > 150 and area<196:
            #        cv2.drawContours(img,[cnt],-1,(0,255,0),2)
            #        cv2.imshow('RGB',img)
            #        cv2.waitKey(1000)
            #        # print(len(cnt))
            #        # print('The Area in green is: ', area)
            #    elif area > 50 and area<90:
            #        cv2.drawContours(img,[cnt],-1,(0,0,255),2)
            #        cv2.imshow('RGB',img)
            #        cv2.waitKey(1000)
            #        # print(len(cnt))
            #        # print('The Area in red is: ', area)
                
                if area < 200 and length > 13 and length < 30 and min_x > 180 and height > 0 and height < 20 :
        #                name = input_dir.split('/')[-1]
#                    print('Image: {}, Area: {}, Length: {}, Height: {} avg_x: {}, avg_y: {}, edges: {}'.format(image, area, length, height, avg_x, avg_y, edges))
                    cv2.drawContours(img,[cnt],-1,(0, 255, 255),2)
                    start_x.append(avg_x)
                    start_min.append(top_x)
                    start_max.append(bottom_x)
                    page_number.append(page)
#                cv2.imshow(image,img)
#                cv2.waitKey(5)
                filename = dir_path + '/' + path_image.split('.')[0] + 'sharp_detected.jpg'
                cv2.imwrite(filename, img)
                    # print('Detected at pixel:{} on page number: {}'.format(avg_x, page))
                
        #                cv2.destroyAllwindows()
        #            # print(edges)
        #            # print('The Area in pink is: ', area)
                
        #            # print('The filename is: ', filename)
                
                cv2.imwrite(filename, img)
    out = pd.DataFrame(list(zip(page_number, start_x, start_min, start_max)), columns =['Page', 'Start', 'Min', 'Max'])    
    
#    out, x, y, page = detect_start(input_directory_path)
    out = out.sort_values(by=['Page', 'Start']).reset_index(drop = True)
    out['X_Pos'] = 0
    x_pos = 0
    


    for i in range(len(out)):
        if i != len(out) -1 and out['Page'][i] == out['Page'][i+1]:
            now = out['Start'][i]
            next_x = out['Start'][i+1]

            sharp = True
            if abs(next_x - now) < 5:
#                out['X_Pos'][i] = x_pos
#                out['X_Pos'][i+1] = x_pos
                out['Start'][i+1] = out['Start'][i]
            if i > 0 and i < len(out) - 1:
                prev_x = out['Start'][i - 1] 
                if abs(next_x - now) < 10 or abs(prev_x - now) < 10:
                    pass
                else:
                    sharp = 'False'
            elif i == 0:
                if abs(next_x - now) > 10:
                    sharp = 'False'
            elif i == len(out) - 1:
                prev_x = out['Start'][i - 1]
                if abs(prev_x - now) > 10:
                    sharp = 'False'
        
            if sharp == 'False':
                    out['Start'][i] = float('nan')
    out['Height'] = float('nan')
    for i in range(len(out)):

        if (i != len(out)-1) and out['Page'][i+1] == out['Page'][i]:
            if out['Start'][i+1] == out['Start'][i]:
                out['Height'][i] = (out['Min'][i] + out['Max'][i+1])/2
                out['Start'][i+1] = float('nan')
                out['Height'][i+1] = float('nan')
                out['Page'][i+1] = float('nan')
                out['X_Pos'][i+1] = float('nan')


    out = out.dropna()
    out = out.sort_values(by=['Page', 'Start', 'Min'],ascending=[True, True, False]).reset_index(drop = True)         
    out['Sharp'] = 'Yes'
    x_pos = 0
    for i in range(len(out)):
        if i < len(out) - 1:
            if out['Page'][i] == out['Page'][i+1]:
                if abs(out['Start'][i] - out['Start'][i+1]) < 40:
                    out['X_Pos'][i] = x_pos
                elif i > 0 and abs(out['Start'][i] - out['Start'][i-1]) < 40:
                    out['X_Pos'][i] = x_pos
                    x_pos += 1
                elif i == 0:
                    out['X_Pos'][i] = x_pos
                else:
                    out['X_Pos'][i] = x_pos
                    x_pos += 1                    
            elif out['Page'][i] != out['Page'][i+1]:
                out['X_Pos'][i] = x_pos
                x_pos = 0
        else:
            out['X_Pos'][i] = x_pos    

#        if (k < len(out)-1) and out['Start'][k+1] - out['Start'][k] < 40 :
#            
#            out['X_Pos'][k] = x_pos
#            out['X_Pos'][k+1] = x_pos
#            
#            k += 2
#        
#        else:
#
#            out['X_Pos'][k] = x_pos
#            k += 1
#            
#        x_pos+=1   
#        try: 
#            if out['Page'][k] != out['Page'][k+1]:
#                out['X_Pos'][k] = x_pos
#                x_pos=0
#                k+=1
#        except:
#            pass

    df =out.reset_index(drop = True)
    df['Note'] = 0
    for i in range(len(df)):
        if i == (len(df) - 1):
            pass
        df['Note'][i] = note_detect(df['Height'][i], df['Sharp'][i], bass)      
    return df


#####################################################################################
   ## note recognition function ##
#####################################################################################
df_note = pd.read_csv("Beats and ties/note_gap.csv")
df_note['Start'] = 0
df_note['End'] = 0

note_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
def notes(transpose = 0):
    df_note['Start'][0] = 458 + 22*transpose
    df_note['End'][0] = 470 + 22*transpose
    for i in range(len(df_note)):
        if i != 0:
            try:
                df_note['Start'][i] = df_note['Start'][i-1] - 22
                df_note['End'][i] = df_note['Start'][i] + 12
            except:
                print(i)
    return df_note
            
def note_detect(height, sharp, bass = False):
    if bass == True:
        trans = 1
    else:
        trans = 0
    df_note = notes(trans)
    height = int(height)
    sharp = sharp
    found = False
    for i in range(len(df_note)):
        offset = 0
        if height > df_note['Start'][i] and height < df_note['End'][i]:
            found = True
            if bass == True:
                offset = 1
            note = df_note['Note'][i-offset]           
            break
        elif i < len(df_note) - 1 and height <= df_note['Start'][i] and height >= df_note['End'][i+1]:
            ref = df_note['Ref'][i] + 1
            if ref == 7:
                ref = 0
            found = True
            try:
                note =  note_list[ref]
            except:
                print(ref)
            break
        else:
            found = False
    if found == False:
        return ('Not Found')
    else:
        if sharp == 'Yes':
            note = note + '#'
            return note
        else:
                return note 
#####################################################################################
   ## Scales Detection ##
#####################################################################################


def real_note(note):
    if note == 'A#': note = 'B \u266D'
    elif note == 'B#': note = 'C'
    elif note == 'C#': note = 'D \u266D'
    elif note == 'D#': note = 'E \u266D'
    elif note == 'E#': note = 'F'
    elif note == 'F#': note = 'G \u266D'
    elif note == 'G#': note = 'A \u266D'
    else: note = note
    return note      
#####################################################################################
   ## Scales Detection ##
#####################################################################################

         
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/IDWTMAT Example L3 Triggers/'
#df = detect_sharp(input_directory_path)
##note_detect(393, 'Yes', False)

     