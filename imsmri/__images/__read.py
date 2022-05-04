from skimage.io import imread

#abre e retorna a matriz de uma imagem recebida no path_file.
def image(path_file):
    return imread(path_file)
