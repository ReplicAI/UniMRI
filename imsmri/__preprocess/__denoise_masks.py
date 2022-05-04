from medpy.filter.smoothing import anisotropic_diffusion as ans_dif
import nibabel as nib
from .. import __path as path
from .. import __files as files

denoise_iter = 3

def process(data):
    """
    Function based on NicMSlesion
    Anisotropic Diffusion (Perona and Malik)
    """
    global denoise_iter

    for mod in ["path_T1", "path_T2", "path_FLAIR"]:
        filename = data[mod+"_pre"] if path.isfile(data[mod+"_pre"]) else data[mod]
        tmp_scan = nib.load(filename)

        tmp_scan.get_data()[:] = ans_dif(tmp_scan.get_data(), niter=denoise_iter)

        tmp_scan.to_filename(
            path.join(path.dirname(data[mod+"_pre"]), "t"+path.lastname(data[mod+"_pre"]))
        )

        files.replace(
            path.join(path.dirname(data[mod+"_pre"]), "t"+path.lastname(data[mod+"_pre"])),
            data[mod+"_pre"]
        )