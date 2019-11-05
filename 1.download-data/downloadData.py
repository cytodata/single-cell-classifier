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

args = parser.parse_args()

downloadData(args.downloadLocation)