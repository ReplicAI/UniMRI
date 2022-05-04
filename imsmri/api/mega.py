from .__mega import __download as __down
from .__mega import __upload as __up

#variaveis para armazenar o objeto de login
__downloader = None
__uploader = None

#usado para não ter que por senha duas vezes pro mesmo email
#essas variaveis salvam os emails usados anteriormente (em tempo de execução)
__email_d, __email_u = "", ""

#essa função faz o login na api mega
def login(email, passwd, download=False, upload=False):
    global __downloader, __uploader, __email_d, __email_u
    #esse try é usado para verificar se o email e senha estão certos, caso não, uma exceção é gerada
    try:
        #se logado para uso de download, a variavel __downloader recebe o objeto da api mega
        if download:
            #caso o ja tenha sido logado para upload e o email for o mesmo, o __downloader aponta para o mesmo objeto do __uploader
            if __email_u == email and __uploader is not None:
                __downloader = __uploader
            else:
                #faz o login no mega
                __downloader = __down.login(email, passwd)
                __email_d = email
        #mesmo caso do download só que para o upload
        if upload:
            if __email_d == email and __downloader is not None:
                __uploader = __downloader
            else:
                __uploader = __up.login(email, passwd)
                __email_u = email
        #caso nenhum dos dois tenham sido definidos, loga como download e upload
        if not download and not upload:
            __downloader = __down.login(email, passwd)
            __uploader = __downloader

    #esse except retorna qualquer problema que tenha acontecido no login
    except Exception as e:
        raise Exception(e)

#upa um diretorio para o mega (não é muito usado, podendo ser removido futuramente)
def upload_folder(path_folder=None):
    global __uploader
    #sempre verifica se está logado no mega ou não
    if __uploader is None:
        raise Exception("upload: No user logged in!")

    return __up.upload_folder(__uploader, path_folder=path_folder)

#upa o diretorio images_out para o mega (usado para guardar as imagens geradas pelo preprocessamento to_slice)
#essa função é necessaria para o funcionamento do parametro continue_from_mega e replace da função run do preprocessamento
def upload_images_out():
    global __uploader
    #sempre verifica se está logado no mega ou não
    if __uploader is None:
        raise Exception("upload: No user logged in!")

    return __up.upload_images_out(__uploader)

#função interna de download dos datasets que estão no mega (no nosso caso)
def __download(data):
    global __downloader
    #sempre verifica se está logado no mega ou não
    if __downloader is None:
        raise Exception("download: No user logged in!")

    return __down.download(__downloader, data)

#função interna de download do arquivo images_out.zip
def __download_images_out(path_to=None):
    global __downloader
    #sempre verifica se está logado no mega ou não
    if __downloader is None:
        raise Exception("download: No user logged in!")

    return __down.download_images_out(__downloader, path_to=path_to)

#recebe um json de informações (metadados [criados no arquivo __init__ do subpacote __preprocess]) e faz o upload dos arquivos depois de pré processados
#nessa função, os dados pré-processados (exames 3D) são upados no mega
#talvez seja outra função a ser removida futuramente (foi criada, pois o pré-processamento demora muito, então é mais facil baixar do que pré-processar novamente)
def __upload(data, folder="Databases_Pre"):
    global __uploader
    #sempre verifica se está logado no mega ou não
    if __uploader is None:
        raise Exception("upload: No user logged in!")

    return __up.upload(__uploader, data, folder)
