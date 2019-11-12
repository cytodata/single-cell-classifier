import os
from zipfile import ZipFile

from .check_if_download_complete import checkIfDownloadComplete


def unzipData(locationData: str):
    """
    locationData: The name of the zip file to extract.
    """
    # Ensure that the file exists and is fully downloaded
    if os.path.exists(locationData):

        fileComplete = checkIfDownloadComplete(locationData)
        assert fileComplete, "Found file seems to be incomplete, please download again"

        with ZipFile(locationData, "r") as zip_fh:
            zip_fh.printdir()
            print("Extracting all files")
            zip_fh.extractall(path="data")

        print("Deleting zip file")
        os.remove(locationData)
    else:
        raise FileNotFoundError(
            "{} does not exist, download first".format(locationData)
        )
