#%%
import tarfile
from io import BytesIO
from PIL import Image
import numpy as np
import os
from pathlib import Path

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
):
    newPlateName = plate.replace("P", "S")
    extracted_file = TARFILE.extractfile(
        f"training/{target}/211_11_17_X_Man_LOPAC_X5_LP_{newPlateName}_{replicate}_{wellName}_{field}_{cell_id}.tiff"
    )
    b = extracted_file.read()

    img = Image.open(BytesIO(b))
    return img


def get_all_images():
    for member in TARFILE.getmembers():
        try:
            path, name = os.path.split(member.name)
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
            extracted_file = TARFILE.extractfile(member)
            b = extracted_file.read()
            img = Image.open(BytesIO(b))

            yield img, plateName, replicate, wellName, field, cell_id, target
        except:
            continue
