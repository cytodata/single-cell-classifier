# K Nearest Neighbors

Attribute a label to each cell based on the K most similar cells in the training set. This simple approach confirms that a similar morphological profile as measured by EBImage indeed corresponds to a similar mechanism of action.

## Naive Attempt

Using [Sklearn KNN Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) we trained an estimator on the [processed training data](../../2.process-data/README.md).

### Parameters

- n_neighbors=5,10,15,25,35,50 **(differ from default)**
- weights='uniform'
- algorithm='auto'
- leaf_size=30
- p=2
- metric='minkowski'
- metric_params=None
- n_jobs=None

### Experiment setup

We run a script to determine model performance and model stability. 
Every time the script is run another results in added to the list. 
These results show what the performance is (the mean) and how stable it get there (the variance).
This can be used to compare different models with each other and conclude if they have different stability. 

### Results

The macro f1-score on the validation set is [0.300 ± 0.010, for 5, 10, 15, 25, 35 or 50 neighbors](results/all_scores.csv). As for [random forest classifiers](../1.random_forest/README.md), this is very low but insightful. The [confusion matrix](results/0/confusion_matrix.png) (here shown for K = 5) shows that classes can be predicted with different accuracies. Because only the similarity (minkowski distance) to the cells in the training set are used, this shows that the overall morphological profiles provided by the EBImage analysis are representative of the underlying mechanism of action of the compounds used to treat the cells.

### Future Steps

- [ ] Balance training data. The model seems to favor classes that are very dominate.  
- [ ] Parameter optimization. Try cross-validation scheme to select a single optimal value for K (the number of neighbors to consider).
