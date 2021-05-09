# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:14:14 2021

@author: gdlar
"""

def remove_puerto_rico(df):
    df = df[df['STATEFIP'] != 72]
    df = df.reset_index(drop=True)
    return df