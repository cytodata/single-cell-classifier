#!/usr/bin/env python
# coding: utf-8

# # K Nearest Neighbors
# Straightforward classification to provide an easily interpretable baseline model.

# ## Load python modules and data

# In[ ]:


# Initialization
import sys
from pathlib import Path
import os

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

basefolder_loc = Path(os.path.abspath('')).parents[1]
sys.path.append(str(basefolder_loc))
from utils import create_metrics, get_auc


# In[ ]:


data_dir = os.path.join(basefolder_loc, "2.process-data", "data")

def load_data(file_name="train_processed.tsv.gz"):
    file_loc = os.path.join(data_dir, file_name)
    data = pd.read_csv(file_loc, sep="\t")
    X = np.array(data.drop(columns=["cell_code", "cell_id", "plate", "well", "target"]))
    Y = np.array(data.target)
    return X, Y


# Training model
X, Y = load_data("train_processed.tsv.gz")

# Validation of model
valX, valY = load_data("test_processed.tsv.gz")


# ## Train and evaluate KNN classifier

# In[ ]:


KNNclf = KNeighborsClassifier(n_neighbors=15)


# In[ ]:


KNNclf.fit(X, Y)


# In[ ]:


prediction = KNNclf.predict(valX)


# In[ ]:


create_metrics(
    prediction, valY, os.path.join(os.path.abspath(''), "results")
)


# For comparison, the most common label (*dopaminereceptor*) is only found in 10% of the test set, so the model perform three times better than random.
# 
#     from collections import Counter
#     max(Counter(valY).values())/len(valY)
# 

# ## ROC curve
# See https://stackoverflow.com/questions/52910061/implementing-roc-curves-for-k-nn-machine-learning-algorithm-using-python-and-sci/52910821 and https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py
# 

# In[ ]:


prediction_proba = KNNclf.predict_proba(valX)


# In[ ]:


resFolder = os.path.join(basefolder_loc, "3.train_ebimage/2.knn/results/")
roc_auc = get_auc(prediction_proba, valY, plot_curve = False,
                  save_location = resFolder)


# In[ ]:


roc_auc

