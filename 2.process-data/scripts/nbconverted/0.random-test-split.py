#!/usr/bin/env python
# coding: utf-8

# # Randomly Split Test Partition from Training
# 
# Randomly split out 10% of the training data into a testing partion to assess model performance during model development.

# In[1]:


import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split


# In[2]:


np.random.seed(123)


# ## Load data that was downloaded in the `1.download-data` module

# In[3]:


data_dir = os.path.join("..", "1.download-data", "data")
os.listdir(data_dir)


# In[4]:


train_file = os.path.join(data_dir, "training_data.csv")
full_train_df = pd.read_csv(train_file)

print(full_train_df.shape)
full_train_df.head()


# ## Split data and write to file

# In[5]:


train_df, test_df = train_test_split(full_train_df,
                                     test_size=0.1,
                                     stratify=full_train_df.target,
                                     random_state=42)


# In[6]:


file = os.path.join("data", "train.tsv.gz")
train_df.to_csv(file, sep='\t', float_format="%.4f", index=False)

file = os.path.join("data", "test.tsv.gz")
test_df.to_csv(file, sep='\t', float_format="%.4f", index=False)


# In[7]:


print(train_df.shape)
print(test_df.shape)


# In[8]:


target_count_df = (
    pd.DataFrame(train_df.target.value_counts()).merge(
        pd.DataFrame(test_df.target.value_counts()),
        left_index=True,
        right_index=True
    )
)

target_count_df.columns = ["train_counts", "test_counts"]

file = os.path.join("results", "target_counts.tsv")
target_count_df.to_csv(file, sep='\t', index=True)

target_count_df

