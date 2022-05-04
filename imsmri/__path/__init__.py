__all__ = ['__path', '__makedir', '__change', '__diference']

from . import __path, __makedir, __change, __diference
from .. import __res as res
import os

#path da pasta res (onde ficam todos os arquivos temporarios usados pelo sistema)
__resource = os.path.abspath(res.__file__)
__resource = os.path.dirname(__resource)

#variaveis que são usadas em todos os sub pacotes
files_zip = "Databases/Original/Compressed"
files_unzip = os.path.join(__resource, "databases")
files_pre = "Databases/Pre"
files_out = "images_out"
mega_source = ""
resource = __resource

#diretórios onde são salvos os jsons
json_file = os.path.join(__resource, "all_data.json")
temp_file = os.path.join(__resource, "temp.json")
images_file = os.path.join(__resource, "images.json")
log_file = os.path.join(__resource, "log.txt")

__backup = [
    files_zip, files_unzip, files_pre, files_out, mega_source, resource,
    json_file, temp_file, images_file, log_file
]

#functions
def verify(path):
    return __path.verify(path)

def join(*args):
    return __path.join(*args)

def dirname(path):
    return __path.dirname(path)

def isfile(path):
    return __path.isfile(path)

def isdir(path):
    return __path.isdir(path)

def lastname(path):
    return __path.lastname(path)

def remove(path):
    return __path.remove(path)

def change(path1, path2, path_root, ini=True, end=False):
    return __change.change(path1, path2, path_root, ini=ini, end=end)

def diference(path_b, path_s):
    return __diference.diference(path_b, path_s)

def mkdirs(data, pre=False, unzip=False):
    global files_out
    if pre and not os.path.isdir(files_out):
        os.makedirs(files_out)
    return __makedir.make_dirs(data, pre=pre, unzip=unzip, path_unzip=files_unzip)

def __reset():
    global files_zip, files_unzip, files_pre, files_out, mega_source, resource
    global json_file, temp_file, images_file, log_file, __backup

    files_zip = __backup[0]
    files_unzip = __backup[1]
    files_pre = __backup[2]
    files_out = __backup[3]
    mega_source = __backup[4]
    resource = __backup[5]
    json_file = __backup[6]
    temp_file = __backup[7]
    images_file = __backup[8]
    log_file = __backup[9]