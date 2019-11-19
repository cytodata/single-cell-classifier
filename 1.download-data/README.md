# Download Data

This module will download the single cell morphology profiles to use in all downstream analyses.
The data are located on [figshare](https://doi.org/10.6084/m9.figshare.10247531.v1) and are from [Breinig et al. 2015](https://doi.org/10.15252/msb.20156400).

**Note:** Processed EBImage profiles are provided in [`2.process-data`](2.process-data).
Only perform these analyses if you wish to work with raw images or raw EBImage morphology profiles.

## Instructions to Reproduce

Make sure you have python installed.

```bash
# Navigate to this directory
cd 1.download-data

# Download and extract all data to the `data` folder and confirm download integrity
./download-pipeline.sh
```
