import matplotlib.pyplot as plt
import numpy as np

#Essa função recebe uma matriz 2D e a plota na tela
def show(img):
    #se a dimensão da imagem for maior que 3, algo está errado
    if len(img.shape) > 3:
        raise TypeError("Invalid shape {} for image data".format(tuple(img.shape)))
    elif img.shape[0] <= 3 and len(img.shape) == 3:
        #esse é o caso de plotar uma imagem carregada como tensor
        #os tensores invertem a matriz, fazendo com que as 3 camadas de cor fiquem na primeira dimensão
        #ex: numpy: [224,224,3]. tensor: [3,224,224]
        aux = img.numpy()
        img = np.ones((aux.shape[1], aux.shape[2], aux.shape[0]))
        img[:,:,0] = aux[0,:,:]
        img[:,:,1] = aux[1,:,:]
        img[:,:,2] = aux[2,:,:]

    #aplica algumas propriedades para melhor visualização da imagem
    barprops = dict(aspect='auto', cmap='binary', interpolation='nearest')
    plt.imshow(img, **barprops)
    #plota a imagem
    plt.show()