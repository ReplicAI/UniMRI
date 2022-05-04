import os

#substitui um arquivo pelo outro, caso o arquivo de destino exista, ele será deletado
def replace(path_file, path_to):
    if os.path.isfile(path_to):
        os.remove(path_to)
    os.rename(path_file, path_to)