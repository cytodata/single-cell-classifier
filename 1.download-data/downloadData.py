from scripts import downloadData
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--downloadLocation",
    type=str,
    default="data",
    dest="downloadLocation",
    help="The account name of the blobStorage where the validation data is stored",
)
parser.add_argument(
    "--downloadUrl",
    type=str,
    default=r"https://ndownloader.figshare.com/files/18501824?private_link=f41918598b1ff5116825",
    dest="downloadUrl",
    help="The account name of the blobStorage where the validation data is stored",
)

args = parser.parse_args()

downloadData(args.downloadLocation, args.downloadUrl)