import urllib.request
import shutil
import os


def downloadData(
    locationData: str = "temp.zip",
    url: str = r"https://ndownloader.figshare.com/files/18501824?private_link=f41918598b1ff5116825",
):
    """
    locationData: The name of the zip file. 
    url: This is the download link. Pasting this link in your browser should tricker a download.
    """
    # Check if path goes to zipfile
    if not locationData.endswith(".zip"):
        locationData = os.path.join(locationData, "fullData.zip")

    # Check if file already exist
    if os.path.exists(locationData):
        print("file already exists. Nothing is downloaded")
        return

    # Make the path if is doesn't already exist
    path = os.path.split(locationData)[0]
    os.makedirs(path, exist_ok=True)

    print("Start downloading the data")
    # Download the zip from from the download link
    with urllib.request.urlopen(url) as response, open(locationData, "wb") as out_file:
        shutil.copyfileobj(response, out_file)