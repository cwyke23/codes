# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 11:39:40 2021

@author: arvin
"""

import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def tie_page(beats, start, length):
    beat = beats
    input_file = 'Beats and ties/tie-{}-beats.csv'.format(beat)
    df = pd.read_csv(input_file)

    df = df.where(df['Length'] == length)
    df = df. where(df['Start'] == start)
    df = df.dropna().reset_index(drop = True)
    if len(df) != 0:
        tie = df['Ties'][0] - 1
    else:
        tie = False
    return tie