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

df['Skill'] = df['Skill'].str.replace(',', '')
df['Skill'] = df['Skill'].str.replace('[', '')
df['Skill'] = df['Skill'].str.replace(']', '')
df['Skill'] = df['Skill'].str.replace('\'', '')




skills_column = df['Skill'].astype(str)
repeated_skills = Counter(" ".join(skills_column).split()).most_common(10000)

'''
We will be using following top skills and will be categorizing remaining skills under Other
SQL
Python
R
Java
C/C++
Tensorflow
JavaScript
Ruby
Jira
'''
df['Database'] =  skills_column.str.contains("SQL", case = False) |description.str.contains("SQL", case = False) | description.str.contains("DB", case = True)  
df['Python'] =  skills_column.str.contains("Python", case = False) 
df['R'] =  skills_column.str.contains("R", case = False) 
df['Java'] =  skills_column.str.contains("Java", case = False) 
df['C/C++'] =  skills_column.str.contains("C/C++", case = False) 
df['Tensorflow'] =  skills_column.str.contains("Tensorflow", case = False) 
df['JavaScript'] =  skills_column.str.contains("JavaScript", case = False)
df['Ruby'] =  skills_column.str.contains("Ruby", case = False) 
df['Jira'] =  skills_column.str.contains("Jira", case = False) 
df['Container'] = skills_column.str.contains("Docer", case = False) | skills_column.str.contains("Kubernetes", case = False)









'''
We try and find the following properties
BA/BS/Bachelor/Bachelor's
Master/Master's
Ph.D/ Phd/ Doctorate
cloud/aws/gcloud/azure
design/designing
research/researching
analytic/analytics/analysis
finance/financial/finances
lead/leadership/leaders
'''

df['BA/BS'] = description.str.contains("BA", case = True) | description.str.contains("BS", case = True) | description.str.contains("Bachelor", case = False) | description.str.contains("Bachelors", case = False) | description.str.contains("Bachelor's", case = False)
df['Masters'] = description.str.contains("Master", case = False) | description.str.contains("Master's", case = False) | description.str.contains("MS", case = True)
df['Ph.D'] = description.str.contains("Ph.D", case = False) | description.str.contains("Phd", case = False) | description.str.contains("Doctorate", case = False)
df['Cloud'] = description.str.contains("cloud", case = False) | description.str.contains("aws", case = False) | description.str.contains("gcloud", case = False) | description.str.contains("azure", case = False)
df['Design'] =  description.str.contains("design", case = False) |description.str.contains("designing", case = False)  
df['Research'] =  description.str.contains("research", case = False) |description.str.contains("researching", case = False)  
df['Analysis'] =  description.str.contains("analytic", case = False) |description.str.contains("analytics", case = False) |description.str.contains("analysis", case = False)  
df['Finance'] =  description.str.contains("finance", case = False) |description.str.contains("financial", case = False) |description.str.contains("finances", case = False)  
df['Lead'] =  description.str.contains("lead", case = False) |description.str.contains("leadership", case = False) |description.str.contains("leaders", case = False)  



testdf = df.iloc[:20,:]
testdescription = df['Description'].astype(str)
testdf['Full'] = testdescription.str.contains("full ", case = False) | testdescription.str.contains("position ", case = False)



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
