# Process Data

The following module processes downloaded data (from [`1.download-data`](1.download-data)).

We use [pycytominer](https://github.com/cytomining/pycytominer) to normalize and select meaningful morphology features in the EBImage profiles.

**Note:** The processed output data of this module is already provided in [`2.process-data/data`](https://github.com/cytomining/pycytominer).
Therefore, the following pipeline is optional to reproduce the full analysis.

## Instructions to Reproduce

```bash
# Navigate to the directory
cd 2.process-data

# Execute all of the notebooks to output processed data
./process-data-pipeline.sh
```
