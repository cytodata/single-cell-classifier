#!/bin/bash
#
# Process the data using methods centered around random forest classifiers
set -e

python ./3.train_ebimage/1.random_forest/random-forest.py
python ./3.train_ebimage/1.random_forest/random-forest-eigenvalues.py
python ./3.train_ebimage/1.random_forest/random-forest-eigenvalues+ebimages.py
python ./3.train_ebimage/1.random_forest/random-forest-selected-eigenvalues+ebimages.py