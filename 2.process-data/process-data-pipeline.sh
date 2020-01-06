#!/bin/bash
#
# Take the data downloaed in 1.download-data and process it for input into downstream
# analysis modules, including machine learning applications.
set -e

# First, convert all notebooks to scripts
jupyter nbconvert --to=script \
  --FilesWriter.build_directory=2.process-data/scripts/nbconverted \
  2.process-data/*.ipynb

# Step 1: Randomly split training data into training and test sets
jupyter nbconvert --to=html \
  --FilesWriter.build_directory=2.process-data/scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute 2.process-data/0.random-test-split.ipynb

# Step 2: Process single cell morphology profiles in the training and test sets
jupyter nbconvert --to=html \
  --FilesWriter.build_directory=2.process-data/scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute 2.process-data/1.process-ebimage-features.ipynb

# Step 3: Process single cell into eigenvalues
python 2.process-data/2.0.process-eigenvalues.py

jupyter nbconvert --to=html \
  --FilesWriter.build_directory=2.process-data/scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute 2.process-data/2.1.analysing-eigen-values.ipynb