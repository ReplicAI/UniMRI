import zipfile as zipf
from .. import __path as path
from shutil import make_archive
import os

#compacta alguma pasta especifica e coloca em algum diretorio especifico
#no caso, essa função é usada para compactar a pasta images_out antes de enviar para o mega
def zip(path_folder, dest_filename):
    if not path.isdir(path.dirname(dest_filename)):
        return False

    if not path.isdir(path_folder):
        return False

    make_archive(dest_filename, 'zip', path_folder)
    return True

#testes:
if __name__ == "__main__":
    zip("/home/wellington/Trabalho/iMRI-Dataset/Databases/Pre/images_out", "/home/wellington/Trabalho/iMRI-Dataset/database/res/images_out")