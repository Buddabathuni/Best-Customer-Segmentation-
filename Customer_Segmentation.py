#!/usr/bin/env python
# coding: utf-8

# In[2]:


#changing the directory of current working directory to the specified path
import os
os.getcwd()
os.chdir(r'F:\projects\Customer Segmentation Project using Python')
os.getcwd()


# In[3]:


#reading the excel file from the specified path
# getting warnnings to ignore them
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

df =pd.read_excel('Online_Retail.xlsx')
print(df.head())
df1 = df


# In[4]:


#exploring the dataset: finding the missing values:
#nunique() = number of unique values
df1.Country.nunique()


# In[5]:


#finding the unique values in Country Column
#unique() = array of unique values
df1.Country.unique()


# In[6]:


#dropping duplicate values in country and CustomerID
customer_country = df1[['Country','CustomerID']].drop_duplicates()

print(customer_country['Country'].value_counts())
#therefore 'United Kingdom' has the higest count of Customers.


# In[7]:


df1 = df1.loc[df1['Country'] == 'United Kingdom']
print(df1)


# In[8]:


#checking the missing values in each column:
df1.isnull().sum(axis=0)
#so there are 133600 missing values in the customer IDs. since we are dealing only with the Customer Id we remove missing values


# In[9]:


#removing issing values in 'Customer ID'
df1 = df1[pd.notnull(df1['CustomerID'])]


# In[14]:


#checking the minimum values of unit price and Quantity:
df1.Quantity.min()
#so removing the negative valuues in Quantity;
df1 = df1[(df1['Quantity']>0)]
df1.shape

df1.info()
#now we are dealing with 354345 rows and 8 columns of data


# In[15]:


#checking unique values for each column:
#getting how many unique values are there in each column:
def unique_counts(df1):
    for i in df1.columns:
        count = df1[i].nunique()
        print(i, ":", count)
unique_counts(df1)


# In[16]:



#adding a column of total Prices:

df1['Total Price'] = df1['Quantity']* df1['UnitPrice']


# In[18]:


#finding the first and last order of dates:
df1['InvoiceDate'].min()


# In[19]:


df1['InvoiceDate'].max()


# In[28]:


#So lets say recency is calculated for a point of time, we take the last invoive date to be  '2011-12-10':
import datetime as dt
NOW = dt.datetime(2011,12,10)

df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])


# In[29]:


#RFM Segmentation
#creating a RFM Table:
rfmTable = df1.groupby('CustomerID').agg({'InvoiceDate': lambda x:(NOW - x.max()).days, 'InvoiceNo': lambda x: len(x),
                                         'Total Price': lambda x: x.sum()})
rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
rfmTable.rename(columns = {'InvoiceDate':'recency',
                          'InvoiceNo':'frequency',
                          'Total Price': 'monetary_value'}, inplace = True)
rfmTable.head()


# In[31]:


#CustomerID : 12346 has frequency : 1, monetory value : $77183.60 and recency of 325 days
#CustomerID : 12747 has frequency : 103, monetory value: $4196.01 and recency : 2days

#lets check the detail of first customer:
first_customer = df1[df1['CustomerID']== 12346.0]
first_customer


# In[34]:


#split the metrics;
quantiles = rfmTable.quantile(q = [0.25,0.5,0.75])
quantiles = quantiles.to_dict()


# In[36]:


#create a segmented RFM Table;
segmented_rfm = rfmTable
#generally lowest recency, highest frequency and monetory amounts are our best customers

def RScore(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
def FMScore(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1


# In[38]:


#adding a segement number to the new created  segmented RFM Table
segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency',quantiles,))
segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency',quantiles,))
segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value',quantiles,))
segmented_rfm.head()


# In[40]:


#adding a column to combine the r_quartile,f_quartile,m_quartile:
segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str) + segmented_rfm.f_quartile.map(str) + segmented_rfm.m_quartile.map(str)
segmented_rfm.head()


# In[51]:


# so ,  the first customer is not our best customer at all.
#Who are the top 10 of our best customers?

best_customers = segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('monetary_value', ascending=False)
# all those customers with RFMScore= '111' are the best customers.
segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('monetary_value', ascending=False).head(10)


# In[52]:


best_customers.to_csv('Best_Customers.csv')


# In[ ]:




