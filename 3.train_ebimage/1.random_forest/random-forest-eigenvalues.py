# %% Initialization
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

basefolder_loc = Path(__file__).parents[2]
sys.path.append(str(basefolder_loc))

from utils import create_metrics

data_dir = os.path.join(basefolder_loc, "2.process-data", "data")


def load_data(file_name="train_eigen_values.tsv.gz"):
    file_loc = os.path.join(data_dir, file_name)
    data = pd.read_csv(file_loc, sep="\t")
    X = np.array(data.drop(columns=["cell_codes", "targets"]))
    Y = np.array(data.targets)
    return X, Y


# %% Training model
RFclf = RandomForestClassifier(n_estimators=100)
X, Y = load_data("train_eigen_values.tsv.gz")
RFclf.fit(X, Y)

# %% Validation of model
valX, valY = load_data("test_eigen_values.tsv.gz")
prediction = RFclf.predict(valX)

create_metrics(
    prediction,
    valY,
    os.path.join(os.path.join(os.path.dirname(__file__)), "results_eigenvalue"),
)
