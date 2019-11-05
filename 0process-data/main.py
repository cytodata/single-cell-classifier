import urllib.request
import shutil
import zipfile
import os
from .download_data import downloadData
import pandas as pd


class DataGenerator:
    def __init__(self, locationZipFile: str = os.path.join("data", "fullData.zip")):
        downloadData(locationZipFile)
        self.locationZipFile = locationZipFile

    def getTrainCsv(
        self, csvFileName: str = "training_data.csv"
    ) -> pd.core.frame.DataFrame:
        zipData = zipfile.ZipFile(self.locationZipFile, "r")
        csvFile = pd.read_csv(zipData.open(csvFileName))
        return csvFile

    def getValidationCsv(
        self, csvFileName: str = "validation_data.csv"
    ) -> pd.core.frame.DataFrame:
        zipData = zipfile.ZipFile(self.locationZipFile, "r")
        csvFile = pd.read_csv(zipData.open(csvFileName))
        return csvFile
