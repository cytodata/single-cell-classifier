#!/usr/bin/env python
# coding: utf-8

# # Analysing the eigen values

# In[1]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


train_data = pd.read_csv(os.path.join("data", "train_eigen_values.tsv.gz"), sep="\t")


# In[3]:


train_data.head()


# ## Scatter plot of the first 2 dimensions

# In[4]:


all_targets = train_data.targets.unique()
sample_per_class = 40

small_train_data = pd.DataFrame(columns=train_data.columns)
targets_mapping = {}
for idx, target in enumerate(all_targets):
    targets_mapping[target] = idx
    small_train_data = pd.concat([small_train_data, train_data.loc[train_data.targets == target].sample(sample_per_class)])

color = small_train_data.targets.replace(targets_mapping).to_numpy()


# In[5]:


from matplotlib import cm

def create_scatter_plot(
    save_location: str,
    eigenvalue1: int = 0,
    eigenvalue2: int = 1,
    sample_per_class: int = 40,
    ):

    fig, ax = plt.subplots(figsize=(9, 8), dpi=80)
    colormap = cm.get_cmap('tab20', 20)

    for idx, target in enumerate(all_targets):
        targets_mapping[target] = idx
        small_train_data = train_data.loc[train_data.targets == target].sample(sample_per_class)
        x = small_train_data["eigen_value_"+str(eigenvalue1).zfill(4)]
        y = small_train_data["eigen_value_"+str(eigenvalue2).zfill(4)]
        color = np.array([colormap(idx)])
        ax.scatter(x, y, c=color, label=target,
                alpha=0.7, edgecolors='none', cmap='tab20')

    ax.legend(loc="upper right", title="Classes")
    ax.grid(True)

    plt.savefig(os.path.join(save_location, f"scatterplot_eigen_value_{str(eigenvalue1).zfill(4)}_eigen_value_{str(eigenvalue2).zfill(4)}.png"))
    plt.close(fig)


# # F-test
# The f-test (ANOVA) calculates if all classes have the same mean value

# In[6]:


from sklearn.feature_selection import f_classif

minimum_p = 0.0005

fvalues, pvalues = f_classif(train_data.drop(columns=['cell_codes', 'targets']), train_data.targets)
independed_eigen = np.where(pvalues < minimum_p)[0]
print(independed_eigen)


# In[57]:


for i in range(0, len(independed_eigen), 2):
    if i == len(independed_eigen) -1:
        create_scatter_plot("results", independed_eigen[i], independed_eigen[-1])
    else:
        create_scatter_plot("results", independed_eigen[i], independed_eigen[i + 1])

