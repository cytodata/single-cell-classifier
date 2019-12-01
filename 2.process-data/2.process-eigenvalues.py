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
all_cell_codes = []
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
    all_targets.append(data[2])
    all_cell_codes.append(data[1])

all_images = np.array(all_images, dtype=np.uint8)
# %% PCA transformation
pca = PCA(n_components=2000)
pca.fit(all_images)
images_pca = pca.transform(all_images)

# %%
plt.figure(1, figsize=(12, 8))

plt.plot(pca.explained_variance_, linewidth=2)

plt.xlabel("Components")
plt.ylabel("Explained Variaces")
plt.show()

# %% save eigen values
file = os.path.join(basefolder_loc, "2.process-data", "data", "train_eigen_values.tsv.gz")
train_df = pd.DataFrame(pd.np.column_stack([all_cell_codes, all_targets, images_pca]))
train_df.to_csv(file, sep='\t', float_format="%.6f", index=False)

# %% load data
test_dataframe = pd.read_csv(
    os.path.join(basefolder_loc, "2.process-data", "data", "test.tsv.gz"),
    sep='\t'
)
image_generator = get_all_images(test_dataframe)

all_images = []
all_targets = []
all_cell_codes = []
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
    all_targets.append(data[2])
    all_cell_codes.append(data[1])

all_images = np.array(all_images, dtype=np.uint8)

# %% pca transformation of test
images_pca = pca.transform(all_images)
# %% save eigen values
file = os.path.join(basefolder_loc, "2.process-data", "data", "test_eigen_values.tsv.gz")
test_df = pd.DataFrame(pd.np.column_stack([all_cell_codes, all_targets, images_pca]))
test_df.to_csv(file, sep='\t', float_format="%.6f", index=False)