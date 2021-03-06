#Importing required python libraries

import pandas as pd
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
import random
#from matplotlib import pyplot as plt





#Data Processing
df = pd.read_csv("indeed_job_dataset.csv")

#Remove unnecessary columns
df = df.drop(['Unnamed: 0','Link','No_of_Skills','Location','Company_Industry'], axis = 1)

#Removing skills kept in the dataset
#This will be populated later by us
df = df.drop(['python','sql','machine learning','r','hadoop','tableau','sas','spark','java','Others'], axis = 1)


#Searching for the most repeating words
description = df['Description'].astype(str)
repeated = Counter(" ".join(description).split()).most_common(10000)

#Scraping Skill column
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
df['Database'] =  skills_column.str.contains("SQL", case = False) | skills_column.str.contains("DB", case = True)  
df['Python'] =  skills_column.str.contains("Python", case = False) 
df['R'] =  skills_column.str.contains("R", case = False) 
df['Java'] =  skills_column.str.contains("Java", case = False) 
df['C/C++'] =  skills_column.str.contains(" C ", case = True) | skills_column.str.contains("C\+\+", case = True) 
df['Tensorflow'] =  skills_column.str.contains("Tensorflow", case = False) 
df['JavaScript'] =  skills_column.str.contains("JavaScript", case = False)
df['Ruby'] =  skills_column.str.contains("Ruby", case = False) 
df['Jira'] =  skills_column.str.contains("Jira", case = False) 
df['Container'] = skills_column.str.contains("Docer", case = False) | skills_column.str.contains("Kubernetes", case = False)


#Scraping Description

'''
We try and find the following properties in Description
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


df = df.replace(True,1)
df = df.drop(['Description'], axis = 1)
df = df.drop(['Skill'], axis = 1)
df = df.drop(['Date_Since_Posted'], axis = 1)



df.insert(1,'CompanyName',df['Company'])
df = df.drop(['Company'], axis = 1)


#Fixing na values
df['Company_Revenue'] = df['Company_Revenue'].fillna('Unknown_company_revenue')
df['Company_Employees'] = df['Company_Employees'].fillna('Unknown_company_employees')
df['CompanyName'] = df['CompanyName'].fillna('Unknown_company_name')
df['No_of_Stars'] = df['No_of_Stars'].fillna(df['No_of_Stars'].mean())
df['No_of_Reviews'] = df['No_of_Reviews'].fillna(df['No_of_Reviews'].median())


# Get one hot encoding of columns 
one_hot_content_job_type = pd.get_dummies(df['Job_Type'])
df = df.drop('Job_Type',axis = 1)
df = df.join(one_hot_content_job_type)

one_hot_content_queried_salary = pd.get_dummies(df['Queried_Salary'])
df = df.drop('Queried_Salary',axis = 1)
df = df.join(one_hot_content_queried_salary)

one_hot_content_company_revenue = pd.get_dummies(df['Company_Revenue'])
df = df.drop('Company_Revenue',axis = 1)
df = df.join(one_hot_content_company_revenue)

one_hot_content_company_employee = pd.get_dummies(df['Company_Employees'])
df = df.drop('Company_Employees',axis = 1)
df = df.join(one_hot_content_company_employee)




#Scaling values
scalerNumReviews = MinMaxScaler()
scalerNumReviews.fit(df[['No_of_Reviews']])
df['No_of_Reviews'] = scalerNumReviews.transform(df[['No_of_Reviews']])

scalerNoStars = MinMaxScaler()
scalerNoStars.fit(df[['No_of_Stars']])
df['No_of_Stars'] = scalerNoStars.transform(df[['No_of_Stars']])


#Using y_toPredict to train the different models
y_toPredict = df.iloc[:,2:]



#Clustering algorithms applied below

#K-Means algorithm
from sklearn.cluster import KMeans

#The following is the elbow method which has been commented out for convinience
# =============================================================================
# k_rng = range(10,100,5)
# sse = []
# for k in k_rng:
#     km = KMeans(n_clusters=k)
#     km.fit(y_toPredict)
#     sse.append(km.inertia_)
#      
# plt.xlabel('K')
# plt.ylabel('Sum of squared error')
# plt.plot(k_rng,sse)
# =============================================================================
#We chose 35
num_cluster = 35
km = KMeans(n_clusters=num_cluster)
km.fit(y_toPredict)
y_predicted = km.fit_predict(y_toPredict)
df['Cluster_From_km']=y_predicted

#Birch Algorithm
from sklearn.cluster import Birch
brc = Birch(n_clusters=35)
brc.fit(y_toPredict)
df['Cluster_From_birch'] = brc.predict(y_toPredict)

#MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans
mbk = MiniBatchKMeans(n_clusters=35)
mbk.fit(y_toPredict)
df['Cluster_From_mbk'] = mbk.predict(y_toPredict)

#AgglomerativeClustering
from sklearn.cluster import AgglomerativeClustering
ac = AgglomerativeClustering(n_clusters=35)
df['Cluster_From_ac'] = ac.fit_predict(y_toPredict)

#Affinity Propagation
from sklearn.cluster import AffinityPropagation
ap = AffinityPropagation(preference=-35)
ap.fit(y_toPredict)
df['Cluster_From_ap'] = ap.predict(y_toPredict)





#Creating lists from different clusters from each clustering algorithm

nameListKmeans = [[None]] * num_cluster
for i in range (0,num_cluster):
    nameListKmeans[i] = list()
for index, row in df.iterrows():
    nameListKmeans[row['Cluster_From_km']].append(row['Job_Title'] +","+row['CompanyName'])
    

nameListBirch = [[None]] * num_cluster
for i in range (0,num_cluster):
    nameListBirch[i] = list()
for index, row in df.iterrows():
    nameListBirch[row['Cluster_From_birch']].append(row['Job_Title'] +","+row['CompanyName'])
    

nameListBatchKMeans = [[None]] * num_cluster
for i in range (0,num_cluster):
    nameListBatchKMeans[i] = list()
for index, row in df.iterrows():
    nameListBatchKMeans[row['Cluster_From_mbk']].append(row['Job_Title'] +","+row['CompanyName'])


nameListAgglomerativeClustering = [[None]] * num_cluster
for i in range (0,num_cluster):
    nameListAgglomerativeClustering[i] = list()
for index, row in df.iterrows():
    nameListAgglomerativeClustering[row['Cluster_From_ac']].append(row['Job_Title'] +","+row['CompanyName'])
    
    
nameListAffinityPropagation = [[None]] * (df['Cluster_From_ap'].max()+1)
for i in range (0,df['Cluster_From_ap'].max()+1):
    nameListAffinityPropagation[i] = list()
for index, row in df.iterrows():
    nameListAffinityPropagation[row['Cluster_From_ap']].append(row['Job_Title'] +","+row['CompanyName'])
    
    


#Experiment
#Testing for each row
    
for i in range(len(df)):
    

    #Testing with existing row
    rowToTest = df.iloc[i,:]
    
    clusterkm = rowToTest['Cluster_From_km']
    clusterbirch = rowToTest['Cluster_From_birch']
    clustermbk = rowToTest['Cluster_From_mbk']
    clusterac = rowToTest['Cluster_From_ac']
    clusterap = rowToTest['Cluster_From_ap']
    
    
    listFromkm = nameListKmeans[clusterkm]
    listFrombirch = nameListBirch[clusterbirch]
    listFrommbk = nameListBatchKMeans[clustermbk]
    listFromac = nameListAgglomerativeClustering[clusterac]
    listFromap = nameListAffinityPropagation[clusterap]
    
    testList1 = list(set(listFromkm) & set(listFrommbk))
    testList2 = list(set(listFrombirch) & set(listFromac))
    testList3 = listFromap
    
    testCombine1 = list(set(testList1) & set(testList2))
    testCombine2 = list(set(testCombine1) & set(testList3))
    
    finalList = testCombine2
    
    if(len(finalList) < 7):
        finalList = testCombine1
    
    if(len(finalList) < 7):
        choice = random.randint(0,1)
        if (choice == 0):
            finalList = testList1
        elif (choice == 1):
            finalList = testList2
            
    if(len(finalList) < 7):
        choice = random.randint(0,3)
        if (choice == 0):
            finalList = listFromkm
        elif (choice == 1):
            finalList = listFrombirch
        elif (choice == 2):
            finalList = listFrommbk
        elif (choice == 3):
            finalList = listFromac
            
    
    
    if(len(finalList) < min):
        min = len(finalList)
        
    if(len(finalList) > max):
        max = len(finalList)
    
print(min)
print(max)


