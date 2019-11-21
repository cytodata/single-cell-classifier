#!/usr/bin/env python
# coding: utf-8

# # Random forest

# In[1]:


import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split


# ## Load data that was downloaded in the 2.process-data
# 

# In[2]:


data_dir = os.path.join("..", "..", "2.process-data", "data")
os.listdir(data_dir)


# In[3]:


train_file = os.path.join(data_dir, 'train_processed.tsv.gz')
train_data = pd.read_csv(train_file, sep='\t')
train_data.head()


# In[4]:


test_file = os.path.join(data_dir, 'test_processed.tsv.gz')
test_data = pd.read_table(test_file, sep='\t')
test_data.head()


# ## Creating the estimator

# In[5]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

RFclf = RandomForestClassifier(n_estimators=1000, max_depth=15,
                             random_state=None)
X = np.array(train_data.drop(columns=['cell_code', 'cell_id', 'plate', 'well', 'target']))
Y = np.array(train_data.target)
RFclf.fit(X, Y)


# ## Validation

# In[6]:


valX = np.array(test_data.drop(columns=['cell_code', 'cell_id', 'plate', 'well', 'target']))
valY = np.array(test_data.target)

results = pd.DataFrame({"prediction": RFclf.predict(valX), "expected": valY})
results.head()


# In[7]:


results['combined'] = results['prediction'] + "_" + results['expected'] 


# In[8]:


conflusion_matrix = results.pivot_table(values='combined', index='prediction', columns='expected', 
                         aggfunc=lambda x: len(x)).fillna(0)
conflusion_matrix


# In[9]:


import seaborn as sns
import matplotlib.pyplot as plt
fig=plt.figure(figsize=(18, 16), dpi= 80, edgecolor='k')

sns.heatmap(conflusion_matrix, annot=True, fmt="g")
plt.show()


# # F1 score

# In[10]:


from sklearn.metrics import f1_score
print(f1_score(results.expected, results.prediction, average='macro'))

