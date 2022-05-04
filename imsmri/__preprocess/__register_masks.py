import platform, os
import subprocess
from .. import __path as path
from .. import __files as files

path_preproc = os.path.abspath(__file__)
path_preproc = os.path.dirname(path_preproc)

niftyreg_path = path.join(path_preproc, "third-party-libs/nicMSlesions/libs/linux/niftyreg")

def process(data):
    """
    - function based on NicMSlesion
    - moving all images to the T1 space
    """

    #rigid registration
    os_host = platform.system()
    reg_exe = 'reg_aladin'

    if os_host != 'Linux':
        raise Exception("The OS system", os_host, "is not currently supported.")

    reg_aladin_path = os.path.join(niftyreg_path, reg_exe)
    subprocess.call(["chmod", "+x", reg_aladin_path])

    for mod in ["path_T2", "path_FLAIR"]:
        try:
            text = "T2" if mod == "path_T2" else "FLAIR"
            path_file = data[mod] if not path.isfile(data[mod+"_pre"]) else data[mod+"_pre"]
            subprocess.check_output([reg_aladin_path, '-ref',
                                    data["path_T1"],
                                     '-rigOnly',
                                     '-flo', path_file,
                                     '-aff', path.join(path.dirname(data["path_T1_pre"]), text + '_transf.txt'),
                                     '-res', path.join(path.dirname(data[mod+"_pre"]), "t"+path.lastname(data[mod+"_pre"]))])

            files.replace(
                path.join(path.dirname(data[mod+"_pre"]), "t"+path.lastname(data[mod+"_pre"])),
                data[mod+"_pre"]
            )
        except Exception as e:
            raise Exception(e)

    #lesion mask is also registered through the T1 space.
    #Assuming that the reference lesion space was FLAIR.
    
    reg_resample_path = path.join(niftyreg_path, "reg_resample")
    subprocess.call(["chmod", "+x", reg_resample_path])

    if data["path_lesion"] != "":
        try:
            path_file = data["path_lesion"] if not path.isfile(data["path_lesion_pre"]) else data["path_lesion_pre"]
            subprocess.check_output([reg_resample_path, '-ref',
                                     data["path_T1"],
                                     '-flo', path_file,
                                     '-trans', path.join(path.dirname(data["path_T1_pre"]), 'FLAIR_transf.txt'),
                                     '-res', path.join(path.dirname(data["path_lesion_pre"]), "t"+path.lastname(data["path_lesion_pre"])),
                                     '-inter', '0'])

            files.replace(
                path.join(path.dirname(data["path_lesion_pre"]), "t"+path.lastname(data["path_lesion_pre"])),
                data["path_lesion_pre"]
            )
        except Exception as e:
            raise Exception(e)