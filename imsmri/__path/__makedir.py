import os
from . import __path
import shutil

#Essa função é responsavel por criar os diretórios usados pelo sistem
#caso definido como 'pre', criará todos os diretórios path_pre do json recebido pelo parametro 'data'
#se for 'unzip', criará a estrutura de diretórios para onde os arquivos compactados irão
#se não for nenhum dos dois, cria o diretório indicado na variavel 'data'
def make_dirs(data, pre=False, unzip=False, path_unzip=None):
    if pre:
        for key in data:
            try:
                if data[key] != "" and "pre" in key and not os.path.isdir(__path.dirname(data[key])):
                    os.makedirs(__path.dirname(data[key]))
            except Exception as e:
                raise Exception(e)

        return True
    elif unzip:
        filename = data["filename"].split(".")[0].replace(" ", "_")
        if not os.path.isdir(os.path.join(path_unzip, data["dataset"], filename)):
            os.makedirs(os.path.join(path_unzip, data["dataset"], filename))
        else:
            return None

        return os.path.join(path_unzip, data["dataset"], filename)

    else:
        if not os.path.isdir(data):
            os.makedirs(data)

        return data