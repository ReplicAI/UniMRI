from . import __dataset, __path, __json, __preprocess

#consts
#databases
#cada variavel serve para poder selecionar os bancos de dados de forma simples
isbi = 'isbi'
miccai08 = 'miccai08'
miccai16 = 'miccai16'
liubliana = 'liubliana'
kirby = 'kirby'
oasis = 'oasis'
ehealth = 'ehealth'
all_databases = "all"

#essas variaveis serão usadas na função select para especificar as caracteristicas dos dados que serão usados
male = "M"
female = "F"
healthy = "healthy"

#acessar dados
#essa variavel aponta para o subpacote __json onde estão as funções para retornar os dados selecionados ou todos os dados
data = __json

#functions serve para apontar para o subpacote __preprocess com o intuito de poder chamar as funções de
#preprocessamento para serem usadas na função sequence
functions = __preprocess

#essas variaveis foram colocadas em classes para deixar mais simples de entender o seu funcionamento
#para chamar essas variaveis: preprocess.view.front e não preprocess.front diretamente.
class view:
    #seleciona qual visão do cérebro vai ser usada na função __preprocess.__init__.to_slice
    front = "front" #:,x,:
    sagittal = "sagittal" #x,:,:
    axial = "axial" #:,:,x

class weighting:
    #seleciona qual ponderamento será usado na função __preprocess.__init__.to_slice
    T1 = "T1"
    T2 = "T2"
    FLAIR = "FLAIR"

class sensitivity:
    #seleciona qual sensibilidade será usada na função __preprocess.__init__.to_slice
    #essa sensibilidade tem a ver com os exames em que contenham mascara de lesão, no caso, os doentes
    #essas variaveis controlam o quanto de "problema" vai ser mostrado nas imagens geradas pelo to_slice
    small = "s"
    medium = "m"
    large = "l"

#__load_ok serve para verificar se a função load foi usada ou não (essa função tem que ser usada em primeiro lugar)
__load_ok = False
#__func é um dicionario que conterá as funções que serão usadas no preprocessamento (escolhidas na função sequence)
__func = {}

#functions
def load(path_datasets, path_pre):
    #Essa função carrega os diretórios para uso, ela vai ser mais explicada no arquivo __dataset
    global __load_ok
    __load_ok = True
    return __dataset.load(path_datasets, path_pre, path_unzip_data=__path.files_unzip, path_mega_source=__path.mega_source)

#select: seleciona os dados que o usuario deseja, como sexo, idade, entre outros
#também será mais explicada no subpacote __json
def select(database=None, sex=None, age=None, ms=None, training=True, test=True, unknown=False):
    return __json.__select(database=database, sex=sex, age=age, ms=ms, training=training, test=test, unknown=unknown)

#sequence serve para definir a sequencia das funções de pré processamento
#também conta com os parametros download/upload para especificar se os dados serão baixados e/ou upados
def sequence(*args, download=True, upload=True):
    global __func, __load_ok
    if not __load_ok:
        raise Exception("Directories not loaded! Use the load function")

    if __json.selected_data() is not None:
        __func = {"funcs": [f for f in args], "download": download, "upload": upload}
    
#esta função inicia o pré processamento, tem mais informações sobre o uso no README e mais detalhes internos no arquivo __dataset
def run(to=-1, init=False, replace=False, continue_from_mega=False):
    global __func
    if not __func:
        raise Exception("Invalid Sequence!")

    return __dataset.run(__func, __json.selected_data(), to, init, replace, continue_from_mega)

#preprocess
#esta função serve como interface para a função __preprocess.__set
def define(max_imgs=10, dim=(), center=True, synchronize=False, format_out="jpg", view="axial", weighting="T2", sensitivity="l"):
    return __preprocess.__set(
        max_imgs = max_imgs,
        dim = dim,
        center = center,
        synchronize = synchronize,
        format_out = format_out,
        view = view,
        weighting = weighting,
        sensitivity = sensitivity
    )