import hashlib


def checkIfDownloadComplete(
    fileLocation: str, expectedHash: str = "6583e93eaee9e1cec8dfb11149099174"
):
    with open(fileLocation, "rb") as fh:
        md5 = hashlib.md5()
        data = fh.read()
        md5.update(data)
        md5sum = md5.hexdigest()
    return md5sum == expectedHash
