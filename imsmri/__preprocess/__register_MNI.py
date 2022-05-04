from .. import __path as path
from .. import __files as files
import os

def generate(*args):
    command = ""
    for v in args:
        command += " " + v

    return command[1:]

path_preproc = os.path.abspath(__file__)
path_preproc = os.path.dirname(path_preproc)

niftyreg_path = path.join(path_preproc, "third-party-libs/nicMSlesions/libs/linux/niftyreg")
MNI_template = path.join(path_preproc, "third-party-libs/MNI_Template/icbm_avg_152_t1_tal_lin.nii.gz")

def process(data):
    """
    Registering to MNI_template
    """

    command01 = generate(
        path.join(niftyreg_path, 'reg_aladin'),
        "-ref", MNI_template,
        "-flo", data["path_T1"],
        "-aff", path.join(path.dirname(data["path_T1_pre"]), "MNI_trafo_Affine.txt"),
        "-res", path.join(path.dirname(data["path_T1_pre"]), "t"+path.lastname(data["path_T1_pre"]))
    )
    
    if os.system(command01):
        raise RuntimeError('program {} failed!'.format(command01))

    files.replace(
        path.join(path.dirname(data["path_T1_pre"]), "t"+path.lastname(data["path_T1_pre"])),
        data["path_T1_pre"]
    )

    for mod in ["path_FLAIR_pre", "path_T2_pre"]:
        command = generate(
            path.join(niftyreg_path, "reg_resample"),
            "-ref", MNI_template,
            "-flo", data[mod] if path.isfile(data[mod]) else data[mod.replace("_pre", "")],
            "-res", path.join(path.dirname(data[mod]), "t"+path.lastname(data[mod])),
            "-aff", path.join(path.dirname(data["path_T1_pre"]), "MNI_trafo_Affine.txt")
        )

        if os.system(command):
            raise RuntimeError('program {} failed!'.format(command))

        files.replace(
            path.join(path.dirname(data[mod]), "t"+path.lastname(data[mod])),
            data[mod]
        )

    if data["path_lesion"] != "":
        command02 = generate(
            path.join(niftyreg_path, "reg_resample"),
            "-ref", MNI_template,
            "-flo", data["path_lesion_pre"] if path.isfile(data["path_lesion_pre"]) else data["path_lesion"],
            "-res", path.join(path.dirname(data["path_lesion_pre"]), "t"+path.lastname(data["path_lesion_pre"])),
            "-aff", path.join(path.dirname(data["path_T1_pre"]), "MNI_trafo_Affine.txt")
        )
        
        if os.system(command02):
            raise RuntimeError('program {} failed!'.format(command02))

        files.replace(
            path.join(path.dirname(data["path_lesion_pre"]), "t"+path.lastname(data["path_lesion_pre"])),
            data["path_lesion_pre"]
        )

