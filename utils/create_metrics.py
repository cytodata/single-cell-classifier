import os

from sklearn.metrics import f1_score

from .metrics import create_confusion_matrix, add_score2excel


def create_metrics(prediction: list, true_y: list, save_location: str):
    os.makedirs(save_location, exist_ok=True)
    all_runs = [
        os.path.join(save_location, o)
        for o in os.listdir(save_location)
        if os.path.isdir(os.path.join(save_location, o))
    ]
    new_run = str(len(all_runs))

    create_confusion_matrix(prediction, true_y, os.path.join(save_location, new_run))

    score = f1_score(true_y, prediction, average="macro")
    add_score2excel(score, os.path.join(save_location, "all_scores.xlsx"))
