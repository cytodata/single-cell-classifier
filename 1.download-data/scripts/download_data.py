import urllib.request
import shutil
import os
from .check_if_download_complete import checkIfDownloadComplete

def downloadData(locationData: str, url: str):
    """
    locationData: The name of the zip file. 
    url: This is the download link. Pasting this link in your browser should tricker a download.
    """
    # Check if path goes to zipfile
    if not locationData.endswith(".zip"):
        locationData = os.path.join(
            locationData, "cytodata_2019_orig_challenge_data.zip"
        )

    # Check if file already exist
    if os.path.exists(locationData):
        fileComplete = checkIfDownloadComplete(locationData)
        if fileComplete:
            print("file already exists. Nothing is downloaded")
            return
        else:
            print("Found file seems to be incomplete")

    # Make the path if is doesn't already exist
    path = os.path.split(locationData)[0]
    os.makedirs(path, exist_ok=True)

    print("Start downloading the data")
    # Download the zip from from the download link
    with urllib.request.urlopen(url) as response, open(locationData, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
