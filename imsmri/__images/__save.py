from skimage import io, transform

#Essa função salva a matriz como imagem em um diretório com o nome e formato recebido pelo parametro 'nome'
#tam é uma tupla usada para redimensionar as imagens (caso usada)
def save_img(name, matriz, tam=()):
    img = matriz

    if tam:
        img = transform.resize(img, tam)

    #salva a imagem
    io.imsave(name, img)