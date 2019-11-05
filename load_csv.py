import pandas as pd
from local_variables import locTrainingData, locValidationData

def load_csv_features():
    # Load data and sort by cell code
    trainingData = pd.read_csv(locTrainingData).sort_values(by=['cell_code'])
    validationData = pd.read_csv(locValidationData).sort_values(by=['cell_code'])

    # make sure all none values fields are removed
    filteredData = trainingData.drop(columns=["replicate", "field", "cell_code", "cell_id", "plate", "well", "target"])
    valfilteredData = validationData.drop(columns=[ "cell_code", "well_code"])

    # normalize data with training data as base
    normalizedTrainData = filteredData.div(filteredData.max())
    normalizedValidation = valfilteredData.div(filteredData.max())

    # targets
    trainingTargets = trainingData.target
    validationLabels = validationData.cell_code

    return normalizedTrainData, trainingTargets, normalizedValidation, validationLabels