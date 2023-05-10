import os
import sys

from launch import is_installed, run, git_clone
from modules.paths import models_path
from modules.sd_models import model_hash
from modules import modelloader
from basicsr.utils.download_util import load_file_from_url

dd_models_path = os.path.join(models_path, "mmdet")

def list_models(model_path):
    model_list = modelloader.load_models(model_path=model_path, ext_filter=[".pth"])

    def modeltitle(path, shorthash):
        abspath = os.path.abspath(path)

        if abspath.startswith(model_path):
            name = abspath.replace(model_path, '')
        else:
            name = os.path.basename(path)

        if name.startswith("\\") or name.startswith("/"):
            name = name[1:]

        shortname = os.path.splitext(name.replace("/", "_").replace("\\", "_"))[0]

        return f'{name} [{shorthash}]', shortname

    models = []
    for filename in model_list:
        h = model_hash(filename)
        title, short_model_name = modeltitle(filename, h)
        models.append(title)

    return models

python = sys.executable

run(f'"{python}" -m pip install lightning-utilities==0.4.0', desc=f"Installing lightning-utilities", errdesc=f"Couldn't install lightning-utilities")
run(f'"{python}" -m pip install pytorch-lightning==1.7.6', desc=f"Installing pytorch-lightning", errdesc=f"Couldn't install pytorch-lightning")

if not is_installed("dlib"):
    run(f'"{python}" -m pip install setuptools', desc="Installing setuptools", errdesc="Couldn't install setuptools")
    run(f'"{python}" -m pip install dlib', desc="Installing dlib", errdesc="Couldn't install dlib")

if not is_installed("mmdet"):
    run(f'"{python}" -m pip install openmim==0.3.5', desc="Installing openmim", errdesc="Couldn't install openmim")
    run(f'"{python}" -m mim install mmcv-full==1.7.1', desc=f"Installing mmcv-full", errdesc=f"Couldn't install mmcv-full")
    run(f'"{python}" -m pip install mmdet==2.27.0', desc=f"Installing mmdet", errdesc=f"Couldn't install mmdet")

if (len(list_models(dd_models_path)) == 0):
    print("No detection models found, downloading...")
    bbox_path = os.path.join(dd_models_path, "bbox")
    segm_path = os.path.join(dd_models_path, "segm")
    load_file_from_url("https://huggingface.co/dustysys/ddetailer/resolve/main/mmdet/bbox/mmdet_anime-face_yolov3.pth", bbox_path)
    load_file_from_url("https://huggingface.co/dustysys/ddetailer/raw/main/mmdet/bbox/mmdet_anime-face_yolov3.py", bbox_path)
    load_file_from_url("https://huggingface.co/dustysys/ddetailer/resolve/main/mmdet/segm/mmdet_dd-person_mask2former.pth", segm_path)
    load_file_from_url("https://huggingface.co/dustysys/ddetailer/raw/main/mmdet/segm/mmdet_dd-person_mask2former.py", segm_path)

git_clone("https://github.com/isl-org/MiDaS.git", "repositories/midas", "midas")
