# %% Initialization
import sys
from pathlib import Path

basefolder_loc = Path(__file__).parents[2]

import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

sys.path.append(str(basefolder_loc))
from utils import create_metrics

data_dir = os.path.join(basefolder_loc, "2.process-data", "data")


def load_data(file_name="train_processed.tsv.gz"):
    file_loc = os.path.join(data_dir, file_name)
    data = pd.read_csv(file_loc, sep="\t")
    X = np.array(data.drop(columns=["cell_code", "cell_id", "plate", "well", "target"]))
    Y = np.array(data.target)
    return X, Y


# %% Training model
RFclf = RandomForestClassifier(n_estimators=100)
X, Y = load_data("train_processed.tsv.gz")
RFclf.fit(X, Y)

# %% Validation of model
valX, valY = load_data("test_processed.tsv.gz")
prediction = RFclf.predict(valX)

create_metrics(
    prediction, valY, os.path.join(os.path.join(os.path.dirname(__file__)), "results_ebimage")
)
