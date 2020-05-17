#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random # library for random number generation
import numpy as np # library for vectorized computation
import pandas as pd # library to process data as dataframes

import json # library to handle JSON files

import matplotlib.pyplot as plt # plotting library
# backend for rendering plots within the browser
get_ipython().run_line_magic('matplotlib', 'inline')

import requests
import lxml.html as lh

from sklearn.cluster import KMeans 
from sklearn.datasets.samples_generator import make_blobs


# Reading the data from the URL provided.

# In[10]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# In[18]:


tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


# In[21]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[22]:


[len(C) for (title,C) in col]


# In[35]:


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
df = df.replace('\n','', regex=True)
df.head()
df.columns = df.columns.str.strip()
df.columns


# Removing the rows where Borough value is not assigned

# In[36]:


df = df[df.Borough != 'Not assigned']


# Updating the Neighborhood column with Borough value where Neighborhood column is empty

# In[51]:


df.loc[df['Neighborhood'] == "", 'Neighborhood'] = df.Borough
df


# In[52]:


df.shape

