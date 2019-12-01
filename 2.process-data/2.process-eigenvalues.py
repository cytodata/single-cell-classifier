# %% Initialization
import sys
from pathlib import Path

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

basefolder_loc = Path(__file__).parents[1]
sys.path.append(str(basefolder_loc))
from utils.load_image import get_all_images

# %% load data
train_dataframe = pd.read_csv(
    os.path.join(basefolder_loc, "2.process-data", "data", "train.tsv.gz"),
    sep='\t'
)
image_generator = get_all_images(train_dataframe)

all_images = []
all_targets = []
all_metadata = []
for data in image_generator:
    # Crop image to center reduce the image to 25%
    original = data[0]
    width, height = original.size  # Get dimensions
    left = width / 4
    top = height / 4
    right = 3 * width / 4
    bottom = 3 * height / 4
    cropped_example = original.crop((left, top, right, bottom))

    # Drop the empty red channel reducing the image to 16.7%
    img_np = np.array(cropped_example)[:, :, 1:]

    # Add everything to lists
    all_images.append(img_np.flatten())
    all_targets.append(data[6])
    all_metadata.append(data[1:6])

all_images = np.array(all_images, dtype=np.uint8)
# %% PCA transformation
pca = PCA(n_components=200)
pca.fit(all_images)
images_pca = pca.transform(all_images)

# %%
plt.figure(1, figsize=(12, 8))

plt.plot(pca.explained_variance_, linewidth=2)

plt.xlabel("Components")
plt.ylabel("Explained Variaces")
plt.show()

# %%
train_feature_select_df = feature_select(
    profiles=train_df,
    features=features,
    operation=["drop_na_columns", "variance_threshold", "correlation_threshold"],
    na_cutoff=0.01,
    corr_threshold=0.95,
    corr_method="pearson",
    freq_cut=0.01,
    unique_cut=0.001,
)


# %%
selected_features = [x for x in train_feature_select_df.columns if x.startswith(eb)]

print(train_feature_select_df.shape)
train_feature_select_df.head()

# %% [markdown]
# ### Subset Test Set with the Selected Features

# %%
file = os.path.join("data", "test.tsv.gz")
test_df = pd.read_csv(file, sep="\t").reindex(
    train_feature_select_df.columns, axis="columns"
)

print(test_df.shape)
test_df.head()

# %% [markdown]
# ## Perform Normalization

# %%
train_normalize_df = normalize(
    profiles=train_feature_select_df, features=selected_features, method="robustize"
)

print(train_normalize_df.shape)
train_normalize_df.head()


# %%
test_normalize_df = normalize(
    profiles=test_df, features=selected_features, method="robustize"
)

print(test_normalize_df.shape)
test_normalize_df.head()


# %%
# Assert that the final dataframes are aligned
pd.testing.assert_index_equal(train_normalize_df.columns, test_normalize_df.columns)

# %% [markdown]
# ## Output Processed Files

# %%
file = os.path.join("data", "train_processed.tsv.gz")
train_normalize_df.to_csv(file, sep="\t", float_format="%.4f", index=False)

file = os.path.join("data", "test_processed.tsv.gz")
test_normalize_df.to_csv(file, sep="\t", float_format="%.4f", index=False)

