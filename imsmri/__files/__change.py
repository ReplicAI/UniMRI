from .. import __path as path
import SimpleITK as sitk
import os

#o ehealth não tem como ser pré-processado pois já está como imagens 2D
__exclusions = ["ehealth"]

#muda a extensão dos arquivos dos datasets para nii.gz
def change_extensions(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return False

    path_walk = path.dirname(data["path_T1"])
    #essa função vai 'andar' por todos os subdiretórios para mudar as extenções dos arquivos

    for dirname, dirnames, filenames in os.walk(path_walk):
        for filename in filenames:
            file = path.join(dirname, filename)
            
            #caso ache algum arquivo .nhdr ou .nii, tranforma para nii.gz

            #nhdr to nii.gz
            if file.endswith(".nhdr"):
                img = sitk.ReadImage(file)
                sitk.WriteImage(img, file[:-5]+".nii.gz", True)
                os.remove(file)
                if path.isfile(file[:-5]+".raw"):
                    os.remove(file[:-5]+".raw")
    
            #nii to nii.gz
            if file.endswith(".nii"):
                img = sitk.ReadImage(file)
                sitk.WriteImage(img, file + ".gz", True)
                os.remove(file)