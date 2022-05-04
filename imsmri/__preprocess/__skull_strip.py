from .. import __path as path
from .. import __files as files
import nibabel as nib
import subprocess, os

path_preproc = os.path.abspath(__file__)
path_preproc = os.path.dirname(path_preproc)

robex_path = path.join(path_preproc, "third-party-libs/nicMSlesions/libs/linux/ROBEX/runROBEX.sh")

def process(data):
    """
    Function based on NicMSlesion
    External skull stripping using ROBEX: Run Robex and save skull
    stripped masks
    """

    t1_im = data["path_T1_pre"] if path.isfile(data["path_T1_pre"]) else data["path_T1"]
    t1_st_im = path.join(path.dirname(data["path_T1_pre"]), "brainmask_skull_strip.nii.gz")

    subprocess.call(["chmod", "777", robex_path])
    subprocess.call(["chmod", "777", path.join(path.dirname(robex_path), "ROBEX")])
    try:
        subprocess.check_output([robex_path,
                                 t1_im,
                                 t1_st_im])
    except Exception as e:
        raise Exception(e)

    brainmask = nib.load(t1_st_im).get_data() > 1
    for mod in ["path_T1", "path_T2", "path_FLAIR"]:
        current_mask = data[mod+"_pre"] if path.isfile(data[mod+"_pre"]) else data[mod]

        current_st_mask = path.join(path.dirname(current_mask), "t"+path.lastname(current_mask))

        mask = nib.load(current_mask)
        mask_nii = mask.get_data()
        mask_nii[brainmask == 0] = 0
        mask.get_data()[:] = mask_nii
        mask.to_filename(current_st_mask)
        files.replace(current_st_mask, data[mod+"_pre"])

    if path.isfile(t1_st_im):
        os.remove(t1_st_im)