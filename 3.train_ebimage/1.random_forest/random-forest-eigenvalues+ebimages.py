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


def load_data(file_names=["train_processed.tsv.gz", "train_eigen_values.tsv.gz"]):
    name_target = "targets"
    datas = []
    for file_name in file_names:
        file_loc = os.path.join(data_dir, file_name)
        data = pd.read_csv(file_loc, sep="\t")
        data= data.rename(columns={"cell_code": "cell_codes", "target": "targets"})
        datas.append(data)
    
    data_combined = datas[0]
    for data in datas[1:]:
        data_combined = pd.merge(data_combined, data)
    X = np.array(data_combined.drop(columns=["cell_id", "plate", "well", "cell_codes", name_target]))
    Y = np.array(data_combined[name_target])
    return X, Y


# %% Loading model

X, Y = load_data(["train_processed.tsv.gz", "train_eigen_values.tsv.gz"])

# %% Training model
RFclf = RandomForestClassifier(n_estimators=100)
RFclf.fit(X, Y)

# %% Validation of model
valX, valY = load_data(["test_processed.tsv.gz", "test_eigen_values.tsv.gz"])
prediction = RFclf.predict(valX)

create_metrics(
    prediction,
    valY,
    os.path.join(os.path.join(os.path.dirname(__file__)), "results_ebimage+eigenvalue"),
)
