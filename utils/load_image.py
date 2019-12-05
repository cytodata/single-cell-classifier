#%%
import tarfile
from io import BytesIO
from PIL import Image
import os
from pathlib import Path
import pandas as pd


basefolder_loc = Path(__file__).parents[1]
TARFILE = tarfile.open(
    os.path.join(basefolder_loc, "1.download-data", "data", "training.tar.gz"), "r:gz",
)


def load_img(
    target: str = "adrenoceptor",
    plate: str = "P1",
    cell_id: int = 1,
    replicate: int = 1,
    wellName: str = "C10",
    field: int = 1,
) -> Image:
    """
    Find the single image that matches on all given parameters.

    Returns: image

    WARNING:
    Use this only if you need to load a single image.
    Every time you run this function it loops over the whole zip file.
    If you need all images use get_all_images.
    """
    newPlateName = plate.replace("P", "S")
    extracted_file = TARFILE.extractfile(
        f"training/{target}/211_11_17_X_Man_LOPAC_X5_LP_{newPlateName}_{replicate}_{wellName}_{field}_{cell_id}.tiff"
    )
    b = extracted_file.read()

    img = Image.open(BytesIO(b))
    return img


def get_all_images(dataframe: pd.dataframe) -> (Image, str, str):
    """
    Creates a generator with all the image that match exactly one row in dataframe.
    The check is done based on target, cell_id, well, plate, field and replicate

    returns: img, cell_code, target
    """
    for member in TARFILE.getmembers():
        path, name = os.path.split(member.name)
        if not name.endswith(".tiff"):
            continue
        path, target = os.path.split(path)
        (
            l211,
            l11,
            l17,
            X,
            Man,
            LOPAC,
            X5,
            LP,
            newPlateName,
            replicate,
            wellName,
            field,
            cell_id,
        ) = name.replace(".tiff", "").split("_")
        plateName = newPlateName.replace("S", "P")

        rows = dataframe.loc[
            (dataframe["target"] == target)
            & (dataframe["cell_id"] == int(cell_id))
            & (dataframe["well"] == wellName)
            & (dataframe["plate"] == plateName)
            & (dataframe["field"] == int(field))
            & (dataframe["replicate"] == int(replicate))
        ]
        if len(rows) == 0:
            continue
        elif len(rows) > 1:
            print("To many rows", rows)

        extracted_file = TARFILE.extractfile(member)
        b = extracted_file.read()
        img = Image.open(BytesIO(b))

        yield img, list(rows.cell_code)[0], target
