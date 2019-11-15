import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

np.random.seed(123)

# Define paths
data_dir = os.path.join("..", "1.download-data", "data")

output_data_dir = "data"
os.makedirs(output_data_dir, exist_ok=True)

result_dir = "results"
os.makedirs(result_dir, exist_ok=True)

train_file = os.path.join(data_dir, "training_data.csv")

# Load full data set
full_train_df = pd.read_csv(train_file)
print(f"Shape of full data set {full_train_df.shape}")

train_df, test_df = train_test_split(
    full_train_df, test_size=0.1, stratify=full_train_df.target
)

# Save trainings set
file = os.path.join(output_data_dir, "train.tsv.gz")
train_df.to_csv(file, sep="\t", float_format="%.4f", index=False)

# Save test set
file = os.path.join("data", "test.tsv.gz")
test_df.to_csv(file, sep="\t", float_format="%.4f", index=False)

# Do target count on training set and test set
train_traget_count = pd.DataFrame(train_df.target.value_counts())
test_traget_count = pd.DataFrame(test_df.target.value_counts())

target_count_df = train_traget_count.merge(
    test_traget_count, left_index=True, right_index=True
)

target_count_df.columns = ["train_counts", "test_counts"]

file = os.path.join(result_dir, "target_counts.tsv")
target_count_df.to_csv(file, sep="\t", index=True)
