#!/bin/bash
#
# Take the data downloaed in 1.download-data and process it for input into downstream
# analysis modules, including machine learning applications.
set -e

# Step 1: Randomly split training data into training and test sets
jupyter nbconvert --to=html \
  --FilesWriter.build_directory=scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute 0.random-test-split.ipynb

# Step 2: Process single cell morphology profiles in the training and test sets
jupyter nbconvert --to=html \
  --FilesWriter.build_directory=scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute 1.process-ebimage-features.ipynb
