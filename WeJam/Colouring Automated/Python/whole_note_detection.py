# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 10:45:07 2021

@author: arvin
"""

import cv2
import numpy as np
import pandas as pd
import os
from os import path
import sys
from bar_detect import detect_bar

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#input_dir = "C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/tempsnip.jpg"

#midi_path = input("Enter the midi path: ")
#midi_path = midi_path.replace("\\", "/")
#midi_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/IDWTMAT Example L3 Triggers.mid'

#input_directory_path = input("Enter the Input Directory: ")
#input_directory_path = input_directory_path.replace("\\", "/") + '/'
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/weirder/'
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/'
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/L1 (no colour)/'
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/4th Jan/'
input_directory_path = 'C:/Users/arvin/Documents/WeJam/projects/Image Processing/Example Image Set/IDWTMAT Example L3 Triggers/Weird/test_input/'

#
#output_directory_path = input('Enter the directory where you would like to store the images: ')
#output_directory_path = output_directory_path.replace("\\", "/") + '/'
#output_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/colour_images_new/'

#for i in image_list:   
#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/17th Dec/' 


def detect_X(input_directory_path):
    start = []
    type_note = [] 
    page_number = []
    height_y = []
    bars = detect_bar(input_directory_path)
    
    #### only for test ####


    dir_path = input_directory_path + 'Note Detects'
    if path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)        
    for path_image in os.listdir(input_directory_path):
        if path_image.endswith(".png"):
#            print('\n',path_image)
            
            input_path = input_directory_path + path_image
            try:
                page = int(path_image.split('-')[-1].split(".")[0])
            except:
                page = int(path_image.split(' ')[-1].split(".")[0])
            
    #        input_dir  ="C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/weirder/New Images 17th Dec-{}.png".format(i)
            
            try: middle = bars['Middle'][page-1];# print('Middle is:{}'.format(middle))
            except: print('Middle bar not found at page {}, please check!'.format(page))
            image = input_path.split('/')[-1]
            # print('\n',image)
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
            blur=cv2.GaussianBlur(img,(1,1),0)
            gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            returns,thresh=cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
            
            contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
            
                area=cv2.contourArea(cnt) #contour area
                
                edges = len(cnt)
                cnt = cnt.reshape(edges, 2)  
                min_x = min(cnt.transpose()[0])
                max_x = max(cnt.transpose()[0])
                width = abs(max_x - min_x)
                avg_x = int((round(max_x + min_x))/2)

                top_y = min(cnt.transpose()[1])
                bottom_y = max(cnt.transpose()[1])
                height = abs(top_y - bottom_y)
                avg_y = (top_y + bottom_y)/2


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
                
                if area > 150 and area < 200 and max_x > 200 and edges >= 25 and width > 18 and bottom_y < 500:
    #                name = input_dir.split('/')[-1]
#                    print('Area: {}, height: {}, width: {}, avg_x: {}, edges: {}'.format(area, height, width, avg_x, edges))
                    cv2.drawContours(img,[cnt],-1,(255, 0, 255),2)
                    start.append(avg_x)
                    height_y.append(avg_y)
                    type_note.append('Minim')
                    page_number.append(page)
                    # print('Detected at pixel:{} on page number: {}'.format(avg_x, page))
        #            cv2.imshow(name,img)
        #            cv2.waitKey(500)
        #            # print(edges)
        #            # print('The Area in pink is: ', area)
                    
        #            # print('The filename is: ', filename)
                    
                    cv2.imwrite(filename, img)
        #    img=cv2.imread(filename)
            # Hollow notes with lines passing through
            blur=cv2.GaussianBlur(img,(3,3),0)
            gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            returns,thresh=cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
            
            contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #    filename = output_dir + image.split('.')[0] + 'detection.jpg'
            
            for cnt in contours:
            
                area=cv2.contourArea(cnt) #contour area
                edges = len(cnt)
                cnt = cnt.reshape(edges, 2)  
                min_x = min(cnt.transpose()[0])
                max_x = max(cnt.transpose()[0])
                avg_x = int((round(max_x + min_x))/2)
                
                top_y = min(cnt.transpose()[1])
                bottom_y = max(cnt.transpose()[1])
                height = abs(top_y - bottom_y)
                avg_y = (top_y + bottom_y)/2
                length = abs(max_x - min_x)
        #        # print('max_x: ', max_x)
        #        # print('The max is: ', max_x)
            #    if area > 150 and area<196 and max_x > 180:
            #        
            #        # print('\nThe contour is: ', cnt)
            #        cv2.imshow('RGB',img)
            #        cv2.waitKey(1000)
            #        # print(edges)
                if max_x > 180 and area > 40 and area < 75 and max_x > 200 and edges >= 10 and height < 10 and length < 20 and bottom_y < 500:
        #            # print('The diff is: ', diff)
        #            # print('\nThe contour is: ', cnt)
                    # print('The Area in red for {} is: {} and the avg_x: {}'.format(image, area, avg_x))
#                    cv2.drawContours(img,[cnt],-1,(0,0,255),2)
                    start.append(avg_x)
                    height_y.append(avg_y)
                    type_note.append('Partial Minim')
                    page_number.append(page)
#                    print('Partial minim!  Page:{}, Area:{}, max_x: {}, length: {}, edges:{}, height: {}'.format(page, area, max_x, length, edges, height))
#                    print('\nDetected at pixel:{} on page number: {} with edges: {} with area: {}\n'.format(avg_x, page, edges, area))
#                    cv2.imshow('RGB',img)
#                    cv2.waitKey(10)
#                    cv2.destroyAllWindows()
        #            
        #            # print(len(cnt))
        #            # print('The Area in Red is: ', area)
        #            # print(str(cnt) + '\n')
                    
            # solid notes
            blur=cv2.GaussianBlur(img,(17,17),0)
            gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            returns,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
            
            contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            
            for cnt in contours:
            
                area=cv2.contourArea(cnt) #contour area
                
                edges = len(cnt)
                cnt = cnt.reshape(edges, 2)  
                min_x = min(cnt.transpose()[0])
                max_x = max(cnt.transpose()[0])
                avg_x = int((round(max_x + min_x))/2)
                length = max_x-min_x
                    
                top_y = min(cnt.transpose()[1])
                bottom_y = max(cnt.transpose()[1])
                height = abs(top_y - bottom_y)
                avg_y = (top_y + bottom_y)/2
                
                if max_x > 180 and edges > 4 and length < 20 and area > 10 and bottom_y < 500:
#                    print('The area of the solid region is:{} in page{} with edges : {}, max_x: {}, min_x: {} and length: {}'.format(area, page,edges, max_x, min_x, length))
                    cv2.drawContours(img,[cnt],-1,(255, 255, 0),2)
                    start.append(avg_x)
                    height_y.append(avg_y)
                    type_note.append('Quarter')
                    page_number.append(page)
#                    print('Cyien! Page:{}, Area:{}, max_x: {}, length: {}, edges:{}, height: {}'.format(page, area, max_x, length, edges, height))
#                     print('Detected at pixel:{} on page number: {}'.format(avg_x, page))
#                    cv2.imshow(image,img)
#                    cv2.waitKey(5)
        #            # print(edges)
        #            # print('The Area in white for {} is: {} and the avg_x: {}'.format(image, area, avg_x))
    #        filename = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/test_Output/' + image.split('.')[0] + '_detected.jpg'

########################## Whole Note ###########################################
############### whole note in white spaces ###############

            blur=cv2.GaussianBlur(img,(3,3),0)
            gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            returns,thresh=cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
            
            contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #    filename = output_dir + image.split('.')[0] + 'detection.jpg'
            
            for cnt in contours:
            
                area=cv2.contourArea(cnt) #contour area
                edges = len(cnt)
                cnt = cnt.reshape(edges, 2)  
                min_x = min(cnt.transpose()[0])
                max_x = max(cnt.transpose()[0])
                avg_x = int((round(max_x + min_x))/2)
                
                top_y = min(cnt.transpose()[1])
                bottom_y = max(cnt.transpose()[1])
                height = abs(top_y - bottom_y)
                avg_y = (top_y + bottom_y)/2
                length = abs(max_x - min_x)
        #        # print('max_x: ', max_x)
        #        # print('The max is: ', max_x)
            #    if area > 150 and area<196 and max_x > 180:
            #        
            #        # print('\nThe contour is: ', cnt)
                if max_x > 180 and area > 215 and area < 300 and length <= 17 and length >= 15 and height <=18 and bottom_y < 500 and edges > 8:
                    if max_x > middle and max_x < middle+30:
                        pass
                    else:
                        cv2.drawContours(img,[cnt],-1,(0, 255, 0),2)
                        start.append(avg_x)
                        height_y.append(avg_y)
                        type_note.append('Whole')
                        page_number.append(page)
    #                    print('Green! Page:{}, Area:{}, max_x: {}, length: {}, edges:{}, height: {}'.format(page, area, max_x, length, edges, height))

                if max_x > 180 and area >= 65 and area <150 and length > 13 and length < 20 and edges > 5 and edges < 20 and height < 9 and bottom_y < 500:
                    cv2.drawContours(img,[cnt],-1,(245, 240, 155),2)
                    start.append(avg_x)
                    height_y.append(avg_y)
                    type_note.append('Partial Whole')
                    page_number.append(page)
#                    print('Page:{}, Area:{}, max_x: {}, length: {}, edges:{}, height: {}'.format(page, area, max_x, length, edges, height))
 
            filename =  dir_path + '/' + image.split('.')[0] + 'note_detected.jpg'
        #    # print('The image to be saved is: ', filename)
            cv2.imwrite(filename, img)
#            cv2.imshow(image,img)
            cv2.waitKey(5)
    start_coord = pd.DataFrame(list(zip(start, height_y, type_note, page_number)), columns =['Start', 'Height', 'Type', 'Page Number'])
    
    ## print(contours)
    

    result_df = start_coord.sort_values(by = ['Page Number', 'Start', 'Height'], ascending=[True, True, False])
    result_df = result_df.reset_index(drop=True)
    for i in range(len(result_df)):
        if result_df['Type'][i] == 'Partial Minim' and i < (len(result_df)-1):
            if result_df['Type'][i+1] == 'Partial Minim':

                if result_df['Start'][i] - result_df['Start'][i+1] < 25:
                    result_df['Start'][i] = (result_df['Start'][i] + result_df['Start'][i+1])/2
                    result_df['Type'][i+1] = float('nan')
            else:
               result_df['Type'][i] =float('nan')
    result_df = result_df.dropna()
    result_df = result_df.reset_index(drop=True)
    for i in range(len(result_df)):
        if i < len(result_df)-1:
            if result_df['Page Number'][i] == result_df['Page Number'][i+1]:
                if abs(result_df['Start'][i] - result_df['Start'][i+1]) < 10:
                    result_df['Start'][i+1] = result_df['Start'][i]
    result_df = result_df.sort_values(by = ['Page Number', 'Start', 'Height'], ascending=[True, True, False])
    result_df = result_df.reset_index(drop=True)

    for i in range(len(result_df)):
        if i < len(result_df)-1:
            if result_df['Page Number'][i] == result_df['Page Number'][i+1]:
                if abs(result_df['Start'][i] == result_df['Start'][i+1]):
                    if abs(result_df['Height'][i+1] - result_df['Height'][i])< 10:
                       result_df['Height'][i] = int((result_df['Height'][i+1] + result_df['Height'][i])/2)  
                       result_df['Height'][i+1] = float('nan')
    result_df = result_df.dropna()                   
    result_df = result_df.sort_values(by = ['Page Number', 'Start', 'Height'], ascending=[True, True, False])
    result_df = result_df.reset_index(drop=True)

    for i in range(len(result_df)):
        if result_df['Type'][i] == 'Partial Whole' and i < (len(result_df)-1):
            if result_df['Type'][i+1] == 'Partial Whole':

                if result_df['Start'][i] - result_df['Start'][i+1] < 25:
                    result_df['Start'][i] = (result_df['Start'][i] + result_df['Start'][i+1])/2
                    result_df['Type'][i+1] = float('nan')
            

    result_df = result_df.dropna()
    result_df = result_df.reset_index(drop=True)
    
#    result = pd.DataFrame(columns = ['Start', 'Height', 'Type', 'Page Number', 'Pos'])
#    result_trial = result_df.reset_index(drop = True)
#    height_list = []
#    page_height_dict = {}
#    for k in np.unique(np.array(page_number)):
#        height_dict = {}
#        temp = result_trial.where(result_trial['Page Number'] == k).dropna()
#        temp = temp.reset_index(drop = True)
#        if len(temp) == 1:
#            x = temp['Start'][0]
#            height_list.append(temp['Height'][0])
#        for i in range(1, len(temp)):
#            
#            if abs(temp['Start'][i] - temp['Start'][i-1]) <=15:
#                temp['Start'][i] = temp['Start'][i-1]
#                x = temp['Start'][i-1]
#                height_list.append(temp['Height'][i-1])  
#                if i == len(temp) - 1:
#                    height_list.append(temp['Height'][i])
#            else:
#                try:
#                    x = temp['Start'][i-1]
#                    height_list.append(temp['Height'][i-1])
#                except:
#                    x = temp['Start'][i]
#                    height_list.append(temp['Height'][i])
#                height_list = sorted(height_list)
#                height_dict.update({x:height_list})
#                height_list = []
#        height_list = sorted(height_list)
#        height_dict.update({x:height_list})
#        height_list = []
#        page_height_dict.update({k:height_dict})
        
################################################################################        
#    for i in range(1, len(temp)):
#        if result_trial['Page Number'][i] == result_trial['Page Number'][i-1]: 
#            if abs(result_trial['Start'][i] - result_trial['Start'][i-1]) <=5:
#                result_trial['Start'][i] = result_trial['Start'][i-1]
#                x = result_trial['Start'][i-1]
#                height_list.append(result_trial['Height'][i-1])
#                if i == len(result_trial) - 1:
#                    height_list.append(result_trial['Height'][i-1])
#            else:
#                x = result_trial['Start'][i-1]
#                height_list.append(result_trial['Height'][i-1])
#                height_list = sorted(height_list)
#                height_dict.update({x:height_list})
#                height_list = []
#        elif i == len(result_trial) - 1:
#            x = result_trial['Start'][i]
#            height_list.append(result_trial['Height'][i])
#            height_list = sorted(height_list)
#            height_dict.update({x:height_list})            
#            page= result_trial['Page Number'][i]
#            page_height_dict.update({page:height_dict})
#                                
#        else:
#            x = result_trial['Start'][i-1]
#            height_list.append(result_trial['Height'][i-1])
#            height_list = sorted(height_list)
#            height_dict.update({x:height_list})            
#            page_prev = result_trial['Page Number'][i-1]
#            page_height_dict.update({page_prev:height_dict})
#            height_dict = {}
#            height_list = []
#    start_dict = {}
    height_dict = {}
    page_height_dict = {}
    
    #for i in image_list:
    for path_image in os.listdir(input_directory_path):
        if path_image.endswith(".png"):
            # print(path_image)
            
            input_path = input_directory_path + path_image
            try:
                page = int(path_image.split('-')[-1].split(".")[0])
            except:
                page = int(path_image.split(' ')[-1].split(".")[0])
#            note_number = []
            average = []
            height_list = []
#            pos = 0
        #    i = int(i)
            df = result_df.where(result_df['Page Number'] == page)
            df =df.dropna()
            df['Pos'] = 1
            df = df.reset_index(drop = True)
    #        avg = df['Start'][0]
            
            for j in range(len(df)):
                average.append(df['Start'][j])  
                height_list.append(df['Height'][j])
                if j != (len(df)-1) and abs((df['Start'][j] - df['Start'][j+1])) < 30:
                    average.append(df['Start'][j+1])
                    height_list.append(df['Height'][j+1])
#                    df['Pos'][j] = pos + 1
#                    df['Pos'][j+1] = pos + 1  
#                elif j != (len(df)-1) and (df['Type'][j] == 'Partial Hollow') and df['Type'][j] != 'Partial Hollow':
#                    break
                else:
                    average_new = np.array(average)
                    average_new = np.unique(average_new)
                    height_new = sorted(np.unique(np.array(height_list)).tolist(), reverse = True)
                    
                    
                    
                    avg = int(round(sum(average_new)/len(average_new)))
                        
                    
#                    note_number.append(avg)
#                    note_pos.append(avg)
#                    note_type.append(df['Type'][j])
#                    page_type.append(page)
                    height_dict.update({avg:height_new})
                    average = []
                    height_list = []
#                    pos += 1
#            start_dict.update({page:note_number})
            page_height_dict.update({page: height_dict})    
            height_dict = {}
#            result = result.append(df)
#        result = result.reset_index(drop = True)
#        out_df = pd.DataFrame(list(zip(page_type, note_pos)), columns =['Page', 'Start'])
#        for i in range(len(result)):
#            if result
    return page_height_dict
#detect_X(input_directory_path)
    