#!/bin/bash

# Step 1 (Optional): Download the data from figshare: https://doi.org/10.6084/m9.figshare.10247531.v1
cd 1.download-data
./download-pipeline.sh
cd ..

# Step 2: Process data to prepare for downstream analyses
./2.process-data/process-data-pipeline.sh 
