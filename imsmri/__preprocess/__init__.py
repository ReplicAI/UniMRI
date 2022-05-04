__all__ = []

from . import __register_masks, __register_MNI, __denoise_masks, __skull_strip, __N4, __to_slice, __ehealth
from .. import __path as path
from .. import __json as json

__exclusions = ["ehealth"]

#variaveis internas de configuração do pré processamento to_slice
__max_imgs = 10
__dim = ()
__center = True
__synchronize = False
__format_out = "jpg"

__view = "axial"
__weighting = "T2"
__sensitivity = "l"

#salva um json na pasta de destino com informações sobre o exame que foi pré processado
def __save_data(data):
    path_to = path.join(path.files_pre, data["original_path"])

    if path.isfile(path.join(path_to, "data.json")):
        return
    elif not path.isdir(path_to):
        path.mkdirs(path_to)

    with open(path.join(path_to, "data.json"), "w") as f:
        json.__dump(json.__file_data(data), f)

    data["path_data"] = path.join(path_to, "data.json")

def register_masks(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return data

    __save_data(data)
    path.mkdirs(data, pre=True)
    return __register_masks.process(data)
    
def register_MNI(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return data

    __save_data(data)
    path.mkdirs(data, pre=True)
    return __register_MNI.process(data)

def denoise_masks(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return data

    __save_data(data)
    path.mkdirs(data, pre=True)
    return __denoise_masks.process(data)

def skull_strip(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return data

    __save_data(data)
    path.mkdirs(data, pre=True)
    return __skull_strip.process(data)

def N4(data):
    global __exclusions
    if data["dataset"] in __exclusions:
        return data

    __save_data(data)
    path.mkdirs(data, pre=True)
    return __N4.process(data)

def to_slice(data):
    global __view, __weighting, __sensitivity, __max_imgs, __dim, __center, __synchronize, __format_out
    global __exclusions

    path.mkdirs(data, pre=True)
    
    if data["dataset"] == "ehealth":
        return __ehealth.process(data, __format_out, __dim)

    return __to_slice.process(
        data,
        view=__view,
        max_imgs=__max_imgs,
        weighting=__weighting,
        center=__center,
        dim=__dim,
        form=__format_out,
        synchronize=__synchronize,
        sensitivity=__sensitivity
    )

#função 'set' serve para mudar qualquer configuração do pré processamento to_slice
def __set(max_imgs=10, dim=(), center=True, synchronize=False, format_out="jpg", view="axial", weighting="T2", sensitivity="l"):
    global __max_imgs, __dim, __center, __synchronize, __format_out, __view, __weighting, __sensitivity
    if type(max_imgs) is not int or max_imgs <= 0:
        if type(max_imgs) is not int:
            raise Exception("Invalid attribute on set() function: attribute 'max_imgs' of type 'int' not "+str(type(max_imgs)))
        else:
            raise Exception("Invalid attribute on set() function: attribute 'max_imgs' out of range (1 to INF)")

    if (type(dim) is not tuple and type(dim) is not list) or (len(dim) != 2 and dim):
        if type(dim) is not tuple and type(dim) is not list:
            raise Exception("Invalid attribute on set() function: attribute 'dim' of type 'tuple or list' not "+str(type(dim)))
        else:
            raise Exception("Invalid attribute on set() function: len(dim) out of range (tamx, tamy)")

    if type(center) is not bool:
        raise Exception("Invalid attribute on set() function: attribute 'center' of type 'bool' not "+str(type(center)))
            
    if type(synchronize) is not bool:
        raise Exception("Invalid attribute on set() function: attribute 'synchronize' of type 'bool' not "+str(type(synchronize)))
    
    if type(format_out) is not str:
        raise Exception("Invalid attribute on set() function: attribute 'format_out' of type 'str' not "+str(type(format_out)))

    if type(view) is not str:
        raise Exception("Invalid attribute on set() function: attribute 'view' of type 'str' not "+str(type(view)))

    if type(weighting) is not str:
        raise Exception("Invalid attribute on set() function: attribute 'weighting' of type 'str' not "+str(type(weighting)))

    if type(sensitivity) is not str:
        raise Exception("Invalid attribute on set() function: attribute 'sensitivity' of type 'str' not "+str(type(sensitivity)))

    
    __max_imgs = max_imgs if type(max_imgs) is int and max_imgs > 0 else __max_imgs
    __dim = dim if (type(dim) is tuple or type(dim) is list) and len(dim) == 2 else __dim
    __center = center if type(center) is bool else __center
    __synchronize = synchronize if type(synchronize) is bool else __synchronize
    __format_out = format_out if type(format_out) is str else __format_out
    __view = view
    __weighting = weighting
    __sensitivity = sensitivity