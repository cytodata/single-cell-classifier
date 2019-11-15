#!/bin/bash

# Step 1: Download the data from figshare: https://doi.org/10.6084/m9.figshare.10247531.v1
cd 1.download-data
./download-pipeline.sh

cd ../2.process-data
./process-data-pipeline.sh