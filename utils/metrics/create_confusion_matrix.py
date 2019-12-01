import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_confusion_matrix(prediction: list, true_y: list, save_location: str):
    """
    This function makes confusion matrix and saves it 
    """
    # Create confusion matrix in pandas
    results = pd.DataFrame({"prediction": prediction, "expected": true_y})
    results["combined"] = results["prediction"] + "_" + results["expected"]
    confusion_matrix = results.pivot_table(
        values="combined",
        index="prediction",
        columns="expected",
        aggfunc=lambda x: len(x),
    ).fillna(0)

    # Create plot
    fig = plt.figure(figsize=(18, 16), dpi=80, edgecolor="k")
    sns.heatmap(confusion_matrix, annot=True, fmt="g")

    os.makedirs(save_location, exist_ok=True)
    plt.savefig(os.path.join(save_location, "confusion_matrix.png"))

    # save pandas confusion_matrix
    confusion_matrix.to_csv(os.path.join(save_location, "confusion_matrix.csv"))
