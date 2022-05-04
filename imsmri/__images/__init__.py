__all__ = []

#tudo é importado com importação relativa, todos os subdiretorios do pacote devem manter a hierarquia atual
from . import __get_info, __separate, __show, __load, __read, __save, __rotate
from . import __separate as __sep
from . import __load as __dataload
from .. import __path as path
from .. import __files as files
import json

#variaveis que armazenarão os dados. Imagens em x e rotulos em y
__x_training = []
__y_training = []

__x_validation = []
__y_validation = []

__x_test = []
__y_test = []

#carrega os dados para serem usados
def __load(Path=None, to_tensor=False, transform=None):
    global __x_training, __y_training, __x_validation, __y_validation, __x_test, __y_test

    #se to_tensor for False, a função de load simples é chamada
    #senão, retarna a função de load_tensor para converter em tensores para uso com o pytorch
    if not to_tensor:
        __x_training, __y_training, __x_validation, __y_validation, __x_test, __y_test = __dataload.load(Path=Path)
        return True
    else:
        return __dataload.load_tensor(Path=Path, transform=transform)

#essa função é interna, não acessivel ao usuario
#ela separa os dados em treinamento, validação e teste e é chamada na função load do arquivo dataloader
def __separate(training=None, validation=None, test=None, path_files=None, from_mega=False):
    return __sep.separate(training=training, validation=validation, test=test, path_files=path_files, from_mega=from_mega)

#retorna as informações dos dados que estão na pasta images_out (função interna)
def __info(Path=None):
    return __get_info.get_info(paths=Path)

#simplesmente uma interface para acessar as variaveis locais que contém os dados
def __get():
    global __x_training, __y_training, __x_validation, __y_validation, __x_test, __y_test
    return __x_training, __y_training, __x_validation, __y_validation, __x_test, __y_test

#foi colocada em uma variavel, pois essa função é chamada dentro de uma classe
#sendo assim, o '__' atrapalha na identificação da função, já que o python substitui o '__' de dentro da classe por 'nome_classe__'
#a classe que chama essa função é a __dataload no arquivo dataloader
get_imgs = __get

#lê uma imagem salva no disco e retorna a sua matriz no formato numpy array
def read(path_file):
    if not path.isfile(path_file):
        return None
    return __read.image(path_file)

#salva uma imagem no disco com a possibilidade de mudar seu tamanho (redimencionar)
def save(path_file, matriz, tam=None):
    return __save.save_img(path_file, matriz, tam=tam)

#plota a imagem na tela usando matlabplot
def show(matriz):
    return __show.show(matriz)

#rotaciona uma imagem
def rotate(img, ang):
    return __rotate.rotate(img, ang)