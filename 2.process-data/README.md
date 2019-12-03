# Process Data

The following module processes downloaded data (from [`1.download-data`](1.download-data)).

## Pycytominer
We use [pycytominer](https://github.com/cytomining/pycytominer) to normalize and select meaningful morphology features in the EBImage profiles.

**Note:** The processed output data of this module is already provided in [`2.process-data/data`](https://github.com/cytomining/pycytominer).
Therefore, the following pipeline is optional to reproduce the full analysis.

## eigenvalues
We also use the eigenvalues of every image.
This is done by interpreting an image as a vector (using flatten).
The image is reduced for memory reasons:
- red channel is removed (this is always empty)
- only the middle is used (cutting of mostly black borders and a total of 75% of the image)

Next up the images are run through PCA model.
The model is fitted using only the images of data/train.txv.gz.
The save model reduces both training and validation data to eigenvalues.
The first 2000 eigenvalues are saved in train_eigen_values.tsv.gz and test_eigen_values.tsv.gz

**Note:** The processed output data of this module is **NOT** provided in [`2.process-data/data`](/2.process-data/data`).
Therefore, the following pipeline always needs to be run locally if one wants to use eigenvalues

## Instructions to Reproduce

```bash
# Navigate to the directory
# Execute all of the notebooks to output processed data
./2.process-data/process-data-pipeline.sh
```
