from .. import __path as path
from .. import __json as json
import zipfile
import tarfile

#descompacta os arquivos originais compactados
def unzip(data):
    #cria o diretorio de destino dos arquivos descompactados
    path_to = path.mkdirs(data, unzip=True)
    #se for None, houve algum problema
    if path_to is None:
        return True

    #tem dois formatos de arquivos compactados entre os bancos de dados usados
    #o zip e o tar.bz2, caso adicione mais algum banco com um formato diferente, terá que ser adicionado aqui
    if ".zip" in data["filename"]:
        with zipfile.ZipFile(path.join(path.files_zip, data["filename"]), "r") as z:
            z.extractall(path_to)
    else:
        with tarfile.open(path.join(path.files_zip, data["filename"]), "r:bz2") as t:
            t.extractall(path_to)

    #o oasis tem uma estrutura de pastas diferente (não segue um padrão como as outras)
    #então ele cria a estrutura de diretórios manualmente com essa função:
    if data["dataset"] == "oasis":
        json.__include__oasis()

#quando a pasta images_out é baixada do mega, ela vem em formato zip, então essa função extrai todos os arquivos em um diretorio especificado
def unzip_images_out(path_zip, path_to=None):
    try:
        with zipfile.ZipFile(path_zip, "r") as z:
            if path_to is not None and path.isdir(path_to):
                z.extractall(path_to)
            else:
                #se não for definido um path, será descompactado na pasta de recursos (subpacote __res)
                z.extractall(path.dirname(path_zip))
    except:
        return False
    return True

#testes:
if __name__ == "__main__":
    if not path.isdir(path.join(path.resource, "images_out")):
        path.mkdirs(path.join(path.resource, "images_out"))
    unzip_images_out("/home/wellington/Trabalho/iMRI-Dataset/database/res/images_out.zip", path_to=path.join(path.resource, "images_out"))
    #zip("/home/wellington/Trabalho/iMRI-Dataset/Databases/Pre/images_out", "/home/wellington/Trabalho/iMRI-Dataset/database/res/images_out")