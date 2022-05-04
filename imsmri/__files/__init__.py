__all__ = []

from . import __replace, __unzip, __change, __find, __zip

#funções internas para descompactar e mudar a extenção dos arquivos
__unzip_io = __unzip.unzip_images_out
__unzip = __unzip.unzip
__change_extensions = __change.change_extensions
__zip = __zip.zip

#serve como interface para a função __replace.replace
def replace(path_file, path_to):
    return __replace.replace(path_file, path_to)

#serve como interface para a função __find.find
def find(path_from, filename, sub_directory=True):
    return __find.find(path_from, filename, sub_directory)