import argparse
import os

from scripts import downloadData, unzipData

parser = argparse.ArgumentParser()

parser.add_argument(
    "--downloadLocation",
    type=str,
    default=os.path.join("data", "cytodata_2019_orig_challenge_data.zip"),
    dest="downloadLocation",
    help="The local directory where the downloaded data will be stored",
)

parser.add_argument(
    "--unzip",
    action="store_true",
    help="include if the downloaded file should be unzipped",
)

args = parser.parse_args()
downloadLocation = args.downloadLocation
unzip = args.unzip

downloadUrl = r"https://ndownloader.figshare.com/files/18501824"
downloadData(downloadLocation, downloadUrl)

if unzip:
    unzipData(downloadLocation)
