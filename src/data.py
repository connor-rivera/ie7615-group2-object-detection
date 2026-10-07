"""Getting the cleaned photos onto the colab server and listing them by split"""
import os
import shutil
import tarfile
import pandas as pd

def unpack_cleaned(tar_path, local_root):
    """Copy the cleaned archive from the drive to the server and unpack it"""
    os.makedirs(local_root, exist_ok=True)
    image_dir = os.path.join(local_root, os.path.basename(tar_path).replace(".tar", ""))
    if not os.path.isdir(image_dir):
        local_tar = os.path.join(local_root, os.path.basename(tar_path))
        shutil.copy(tar_path, local_tar)
        with tarfile.open(local_tar) as tar:
            tar.extractall(local_root, filter = "data")
    return image_dir

def load_photos(manifest_csv, image_dir):
    """Kept photos form the manifest with a full path and a YOLO class for each"""
    m = pd.read_csv(manifest_csv)
    m = m[m["keep"]].copy()
    m["path"] = image_dir + "/" + m["relpath"]
    m["yolo_class"] = m["class_id"].astype(int) - 1
    return m.reset_index(drop=True)

def split_pools(photos, split):
    """The background photos and object photos that belong to one split"""
    s = photos[photos["split"] == split]
    return s[s["is_background"]], s[~s["is_background"]]
