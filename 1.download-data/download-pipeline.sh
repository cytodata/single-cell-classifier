#!/bin/bash
set -e

# Download and extract contents of training and validation data located here:
# https://doi.org/10.6084/m9.figshare.10247531.v1
python downloadData.py --unzip

# Confirm download integrity
md5sum -c md5sums.txt
