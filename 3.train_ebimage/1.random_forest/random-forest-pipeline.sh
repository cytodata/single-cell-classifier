#!/bin/bash
#
# Process the data using methods centered around random forest classifiers
set -e

# Run the notebook
jupyter nbconvert --to=html \
  --FilesWriter.build_directory=scripts/html \
  --ExecutePreprocessor.kernel_name=python \
  --ExecutePreprocessor.timeout=10000000 \
  --execute random_forest.ipynb
  
