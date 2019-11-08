from scripts import downloadData
import argparse
import os


parser = argparse.ArgumentParser()

parser.add_argument(
    "--downloadLocation",
    type=str,
    default=os.path.join("..", "data", "cytodata_2019_orig_challenge_data.zip"),
    dest="downloadLocation",
    help="The local directory where the downloaded data will be stored",
)

args = parser.parse_args()
downloadUrl = r"https://ndownloader.figshare.com/files/18501824"
downloadData(args.downloadLocation, downloadUrl)
