import numpy as np

from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from scipy import interp

import matplotlib.pyplot as plt

def get_auc(prediction: np.ndarray, true_y: list, average: str = "both",
            save_location: str = "results/", plot_curve: bool = "true"):
    """
    Get Receiving operator characteristics area under the curve
    for a probabilistic multiclass prediction.
    Values for the 'average' parameter can be set to 'none', 'micro',
    'macro' or 'both' (default).
    """
    
    # From Scikit learn KNeighborsClassifier's predict_proba methods:
    # "Classes are ordered by lexicographic order."
    # So we binarize the true labels similarly
    binLabels = label_binarize(true_y, classes = np.sort(np.unique(true_y)))
    
    # Make sure predictions include all labels
    assert binLabels.shape[1] == prediction.shape[1]

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(prediction.shape[1]):
        fpr[i], tpr[i], _ = roc_curve(binLabels[:, i], prediction[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    if plot_curve:
        # Plot all ROC curves
        plt.figure()

    if average in ["micro", "both"]:
        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(binLabels.ravel(), prediction.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"]) 

        if plot_curve:
            plt.plot(fpr["micro"], tpr["micro"],
            label='micro-average ROC curve (area = {0:0.2f})'
                  ''.format(roc_auc["micro"]),
            color='deeppink', linestyle=':', linewidth=4)

    if average in ["macro", "both"]:
        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(prediction.shape[1])]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(prediction.shape[1]):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= prediction.shape[1]

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        if plot_curve:
            plt.plot(fpr["macro"], tpr["macro"],
            label='macro-average ROC curve (area = {0:0.2f})'
                  ''.format(roc_auc["macro"]),
            color='navy', linestyle=':', linewidth=4)

    if plot_curve:
        colors = plt.cm.get_cmap('tab20')
        for i, color in zip(range(prediction.shape[1]), 
                            colors([x for x in range(prediction.shape[1])])):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                     label='ROC curve of class {0} (area = {1:0.2f})'
                     ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Some extension of Receiver operating characteristic to multi-class')
        plt.legend(loc="lower right")
        plt.show()

    return(roc_auc)