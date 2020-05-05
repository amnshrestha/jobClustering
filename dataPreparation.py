#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:52:38 2020

@author: amanshrestha
"""

import pandas as pd
from collections import Counter





df = pd.read_csv("indeed_job_dataset.csv")
df = df.drop(['Unnamed: 0','Link','No_of_Skills','Location','Company_Industry'], axis = 1)


description = df['Description'].astype(str)
repeated = Counter(" ".join(description).split()).most_common(10000)




df = df.drop(['Description'], axis = 1)





df['Company_Employees']=df['Company_Employees'].str.replace(',','')







df.to_csv('newOne.csv')

# =============================================================================
# file = open("indeed_job_dataset.csv","r")
# content = file.read()
# 
# content = content.replace("\"","")
# content = content.replace("\'","")
# 
# f = open("fixed.csv", "a")
# f.write(content)
# f.close()
# 
# 
# test = "\"Aman is Awesome\""
# test = test.replace("\"","quotes")
# =============================================================================