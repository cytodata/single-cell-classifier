# random forest

Random forest, collection of random generated desicion trees, is a form of classifier. The classification always goes via a hard cut in a feature. This work well if all features are independed.

## naive attempt

Using [Sklearn Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) an estimator is trained on the [processed training data](../2.process-data/README.md).

### parameters
- n_estimators=1000 **(differ from default)**
- criterion=’gini’
- max_depth=15 **(differ from default)**
- min_samples_split=2
- min_samples_leaf=1
- min_weight_fraction_leaf=0.0
- max_features=’auto’
- max_leaf_nodes=None
- min_impurity_decrease=0.0
- min_impurity_split=None
- bootstrap=True
- oob_score=False
- n_jobs=None
- random_state=None
- verbose=0
- warm_start=False
- class_weight=None

### results
The balance f1-score on the validation set is [0.328](scripts/html/random_forest.html). This is very low, but what is interesting is the [confusion matrix](scripts/html/random_forest.html). The prediction are dominated by 3 classes: dopaminereceptor, EGFR, ROCK. When looking at the [most common classes](../2.process-data/results/target_counts.tsv) we find the same 3 classes.
When we look at the next 3 most common classes most common class (adrenoceptor, DNA_intercalation, AMPA) we see very few predictions. Almost all of these images are labeled as one of the 3 dominated classes.
There are a few classes (e.q. Ca2, Cdc25, eNos, rac1) are well predicted and seems to be easy cases.

### future steps
- [ ] Balance training data. The model seems to favor classes that are very dominate.  
- [ ] parameter optimization. Try different parameters to find best solution