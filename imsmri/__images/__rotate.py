from skimage import transform

#rotaciona a imagem
def rotate(img, ang):
    return transform.rotate(img, ang)