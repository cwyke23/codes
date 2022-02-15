# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:13:52 2021

@author: arvin
"""

from music21 import *

tm1 = tempo.MetronomeMark(number=60)

mylist = []


def change_to_60(midifile):

    mymid = converter.parse(midifile)
    tm1 = tempo.MetronomeMark(number=60)
    mylist = []
    
    for l in mymid[0].getElementsByClass('MetronomeMark'):
        mylist.append(l)

    for i in range(len(mymid[0])):
        if mymid[0][i] in mylist:
            mymid[0].pop(i)
            mymid[0].insert(0, tm1)
            fp = mymid.write('midi', fp=midifile)
    return None