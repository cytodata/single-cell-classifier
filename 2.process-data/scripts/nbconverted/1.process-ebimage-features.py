#!/usr/bin/env python
# coding: utf-8

# # Process EBImage-based Features
# 
# We extracted single-cell features from all images using [EBImage](https://github.com/aoles/EBImage).
# These features were acquired from DNA and actin channels and represent various morphology phenotypes.
# 
# Please view the [EBImage reference manual](https://bioconductor.org/packages/release/bioc/manuals/EBImage/man/EBImage.pdf) for a description of all features.
# 
# Many of these features have large differences in distributions, are redundant (highly correlated with each other), have low variance, or have a large proportion of missing values.
# 
# In this notebook, we use [pycytominer](https://github.com/cytomining/pycytominer) to select features and normalize training and test data used in downstream analyses.
# 
# ## Processing Steps
# 
# 1. Remove features that have high missingness
#   * Remove features that have a proportion of missing values greater than 1%
# 2. Remove redundant features (high correlation)
#   * Remove features that have correlations with other features greater than 0.95 Pearson correlation
#   * Retain the feature with the lowest correlation in each highly correlated block of features
# 3. Remove low variance features
#   * Remove features with a ratio of second most common value / most common less than 1%
#     * Removes features that have a common and high outlier
#   * Remove features with a ratio of second max count / max count less than 0.1%
#     * Removes features that have a very high number of redundant values
# 4. Apply robust normalization
#   * subtract median and divide by IQR
#   * robust to outliers
# 
# **Note:** Feature selection applied to the training set is used to select features in the test set, but the training and test sets are normalized separately.

# In[1]:


import os
import pandas as pd

from pycytominer.feature_select import feature_select
from pycytominer.normalize import normalize


# In[2]:


file = os.path.join("data", "train.tsv.gz")
train_df = pd.read_csv(file, sep='\t')

print(train_df.shape)
train_df.head()


# ## Perform Feature Selection

# In[3]:


eb = ("actin", "DNA", "dist", "nuclear")
features = [x for x in train_df.columns if x.startswith(eb)]


# In[4]:


train_feature_select_df = feature_select(
    profiles=train_df,
    features=features,
    operation=["drop_na_columns", "variance_threshold", "correlation_threshold"],
    na_cutoff=0.01,
    corr_threshold=0.95,
    corr_method="pearson",
    freq_cut=0.01,
    unique_cut=0.001
)


# In[5]:


selected_features = [x for x in train_feature_select_df.columns if x.startswith(eb)]

print(train_feature_select_df.shape)
train_feature_select_df.head()


# ### Subset Test Set with the Selected Features

# In[6]:


file = os.path.join("data", "test.tsv.gz")
test_df = pd.read_csv(file, sep='\t').reindex(train_feature_select_df.columns, axis='columns')

print(test_df.shape)
test_df.head()


# ## Perform Normalization

# In[7]:


train_normalize_df = normalize(
    profiles=train_feature_select_df,
    features=selected_features,
    method="robustize"
)

print(train_normalize_df.shape)
train_normalize_df.head()


# In[8]:


test_normalize_df = normalize(
    profiles=test_df,
    features=selected_features,
    method="robustize"
)

print(test_normalize_df.shape)
test_normalize_df.head()


# In[9]:


# Assert that the final dataframes are aligned
pd.testing.assert_index_equal(train_normalize_df.columns, test_normalize_df.columns)


# ## Output Processed Files

# In[10]:


file = os.path.join("data", "train_processed.tsv.gz")
train_normalize_df.to_csv(file, sep='\t', float_format="%.4f", index=False)

file = os.path.join("data", "test_processed.tsv.gz")
test_normalize_df.to_csv(file, sep='\t', float_format="%.4f", index=False)

