# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:06:41 2020

@author: arvin
"""

import cv2
import os 
import numpy as np
import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#input_directory_path = 'C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Images(Uncoloured)/17th Dec/'
def detect_bar(input_dir):
    # Load image, convert to grayscale, Otsu's threshold
    count = 0
    i = 0
    error = []
    bar = False
    #coord = pd.DataFrame(columns = ['Start', 'End'])
    ending = True
    start = []
    end = []
    index = 0
    
    for path_image in os.listdir(input_dir):
        if path_image.endswith(".png"):
            input_path = input_dir + path_image
            
            image = cv2.imread(input_path, -1)
            image = cv2.resize(image, (1920, 600))
            alpha = image[:,:,3] # extract it
            binary = ~alpha
            
            filename = 'temp.jpg'
            
            cv2.imwrite(filename, binary)
            image = cv2.imread(filename)
            
            
            result = image.copy()
            
            
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (1920, 600))
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            
            
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
            detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
            cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
            #    cv2.drawContours(result, [c], 0, (255, 0, 0), 2)
                length = len(c)
                c = c.reshape(length, 2)
                c = np.sort(c, axis = 0)
                left = c[0][0]
                right = c[-1][0]
                
                for j in range(0,length-1):
                    
                    top = c[j][1]
                    bottom = c[j+1][1]
                    diff = abs(bottom-top)
                    if diff >= 70:
                        bar = True
                        break
                    elif int(right - left) >= 2 and diff >= 50 and diff <= 60:
                        cv2.drawContours(result, [c], 0, (0,255, 0), 2)
                        break
                        
                        
                if  int(right - left) == 4 or int(right - left) == 5  and bar == True:
                    
                    cv2.drawContours(result, [c], 0, (0,0,255), 2)
                    if count < 2:
                            
                        if ending == True:
                            end.append(left)
                            ending = False
                        else:
                            start.append(right)
                            ending = True
                        
                    
                    count += 1
            #    if int(bottom[0][1] - top[0][1]) <= 100 and int(bottom[0][1] - top[0][1]) >= 60:
            #        cv2.drawContours(result, [c], -1, (0,0,255), 2)
            #    elif int(bottom[0][1] - top[0][1]) >=52 and int(bottom[0][1] - top[0][1]) <= 60:
            #        cv2.drawContours(result, [c], -1, (255,0,0), 2)    
            
    #           
    #        cv2.imshow('Vertical', result)
    #        cv2.waitKey()
    #        
            if count == 2:
                pass 
            elif count == 1:
                print('Failed, Page:{} left: {}, right{}'.format(path_image, left, right))
#                if  int(right - left) == 4 or int(right - left) == 5:
#                end.append(left)
                start.append(end[-1])
            else:

                break
                error.append(c)
#                print('Error: ' + str(i+1) + ' on page number:' + path_image + 'with count:' + str(count))
#                cv2.imshow(path_image, result)
#                cv2.waitKey(10)
                
                i += 1
        count = 0
        index += 1
        
    coord = pd.DataFrame(list(zip(start, end)), columns =['Middle', 'End'])
    return coord
