from . import __images
from . import __path
import numpy as np
import os

#__dataloader é usada para gerenciar os dados carregados
#quando os dados são carregados pela função load, a instancia dessa classe é atualizada como os dados carregados
class __dataload:
    def __init__(self):
        #self.__loaded serve para controlar se os dados já foram carregados ou não
        self.__loaded = False

        #essas variaveis são as variaveis que conterão todos os dados
        self.__x_training = []
        self.__y_training = []
        self.__x_validation = []
        self.__y_validation = []
        self.__x_test = []
        #quando os dados de test não tem rótulo, serão colocados como None
        self.__y_test = []

    def __load(self):
        #quando essa função é chamada (ver __getattr__) ela carrega os dados chamando a função image.get_imgs()
        global image
        self.__loaded = True
        self.__x_training, self.__y_training, self.__x_validation, self.__y_validation, self.__x_test, self.__y_test = image.get_imgs()

    def __getattr__(self, name):
        #a função __load poderia se chamar load diretamente, porém, para que todas as funções internas tenham um __
        #na frente, o __getattr__ é quem vai chamar a função __load caso o atributo 'load' seja chamado (mas ele não será listado nas funções externas quando os usuarios usarem)
        if name == "load":
            return self.__load()

        raise AttributeError("'__dataload' object has no attribute '%s'" % name)

    def items(self):
        #se os dados não foram carregados, gerará uma exceção
        if not self.__loaded:
            raise Exception("Unloaded data.")

        #retornará todos os dados em duas unicas listas, uma com as imagens e outra com os rótulos
        x_all, y_all = [], []
        x_all.extend(self.__x_training)
        x_all.extend(self.__x_validation)
        x_all.extend(self.__x_test)

        y_all.extend(self.__y_training)
        y_all.extend(self.__y_validation)
        y_all.extend(self.__y_test)

        #retornará no formato numpy array para maior compatibilidade
        return np.array(x_all), y_all

    def training(self):
        if not self.__loaded:
            raise Exception("Unloaded data.")

        #retornará somente os dados de treino
        return np.array(self.__x_training), self.__y_training

    def validation(self):
        if not self.__loaded:
            raise Exception("Unloaded data.")

        #retornará somente os dados de validação
        return np.array(self.__x_validation), self.__y_validation

    def test(self):
        if not self.__loaded:
            raise Exception("Unloaded data.")

        #retornará somente os dados de teste
        return np.array(self.__x_test), self.__y_test

    def __str__(self):
        #quando o objeto dessa classe for usado no print (ou convertido em string), retornará a quantidade de exames carregados
        return "<training: %d, validation: %d, test: %d>" %(len(self.__x_training), len(self.__x_validation), len(self.__x_test))

#objeto da classe __dataload
data = __dataload()
#image aponta para o subpacote __images
image = __images

#load carrega os dados para uso e já faz a separação dos mesmos
#os dados podem ser carregados diretamente da api mega e tranformados em tensores para uso no pytorch
def load(path_imgs=None, tr=None, val=None, ts=None, to_tensor=False, transform=None, from_mega=False):
    global data

    #verifica se o path de saida das imagens pré-processadas existe e foi definido
    #se sim, a função load procurará as imagens no mesmo path (caso o parametro path_imgs seja nulo)
    #caso não, a função procurará no diretório onde a api mega faz o download dos dados
    if os.path.isabs(__path.files_pre):
        __path.files_out = __path.join(__path.files_pre, "images_out")
    else:
        __path.files_out = __path.join(__path.resource, "images_out")

    #caso from_mega seja definido como True, o path padrão será onde a api baixa os dados
    if from_mega:
        __path.files_out = __path.join(__path.resource, "images_out")

    #faz a separação dos dados entre treinamento, validação e teste
    __images.__separate(training=tr, validation=val, test=ts, path_files=path_imgs, from_mega=from_mega)

    #foi criado dois carregamentos diferentes, um quando o to_tensor é True e outro quando é False
    #caso seja False, faz o carregamento simples e retorna o objeto da classe __dataload com os dados
    if not to_tensor:
        __images.__load(Path=path_imgs, to_tensor=to_tensor, transform=transform)
        data.load
        return data

    #caso for to_tensor for True, os dados serão carregados duas vezes, uma para retornar os tensores e outra para fazer o load padrão
    path_f, train_set, val_set, test_set = __images.__load(Path=path_imgs, to_tensor=to_tensor, transform=transform)
    __images.__load(Path=path_f, to_tensor=False, transform=False)
    data.load

    return train_set, val_set, test_set