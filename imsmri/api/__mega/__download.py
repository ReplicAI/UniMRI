from ... import __files
from ... import __path as path
from .__functions import find_file, get_code
from mega import Mega
import shutil

#faz o login no mega. Quando o usuario ou senha estão incorretos, uma exceção é gerada
def login(email, passwd):
    #instancia a classe
    mm = Mega()
    try:
        #faz o login
        obj = mm.login(email, passwd)
        return obj
    except:
        raise Exception("downloader: Invalid Email or Password!")

#faz o download do arquivo zip do banco de dados
def download(obj_mega, data):
    #recebe o metadado do exame, e busca o arquivo compactado no mega
    file = find_file(obj_mega, path.join(path.mega_source, data["filename"]))
    #se não existir esse arquivo, uma exceção é gerada
    if file is None:
        raise Exception("downloader: '%s' file not found in Mega!" % data["filename"])

    #verifica se esse arquivo ainda não foi baixado anteriormente, se não foi, baixa o arquivo
    if not path.isfile(path.join(path.files_zip, data["filename"])):
        obj_mega.download((file['h'], file), dest_path=path.files_zip)
    return file

#faz o download do arquivo zip contendo as imagens geradas pelo to_slice (images_out.zip)
def download_images_out(obj_mega, path_to=None):
    #path_to é para onde a pasta será descompactada
    #verifica se o path_to é um diretorio existente
    if path_to is not None and not path.isdir(path_to):
        return False
    #se não foi definido o path_to, coloca o path de recursos padrão
    elif path_to is None:
        path_to = path.resource

    #procura o arquivo no mega
    file = find_file(obj_mega, "images_out.zip")
    #se não existir, retorna False
    if file is None:
        return False

    #se o arquivo já existe, é apagado e será baixado novamente
    if path.isfile(path.join(path_to, "images_out.zip")):
        path.remove(path.join(path_to, "images_out.zip"))

    #faz o download
    obj_mega.download((file['h'], file), dest_path=path_to)

    #se a pasta onde os arquivos descompactados images_out existe, ela será excluida para ser substituida
    #mas se não existe, é criada
    if not path.isdir(path.join(path_to, "images_out")):
        path.mkdirs(path.join(path_to, "images_out"))
    else:
        shutil.rmtree(path.join(path_to, "images_out"))
        path.mkdirs(path.join(path_to, "images_out"))

    #descompacta o arquivo zip (unzip_IO = unzip_Images_Out)
    __files.__unzip_io(path.join(path_to, "images_out.zip"), path_to=path.join(path_to, "images_out"))
    return file

#essa função não é usada, porem futuramente pode ser
#ela faz o download recursivo de todos os arquivos de algum diretorio dentro do mega
def __download_rec(obj_mega, code, path_to):
    #obtem a lista de arquivos dentro da pasta (o code recebido é o codigo da pasta)
    list_files = obj_mega.get_files_in_node(code)
    for key in list_files:
        #para cada arquivo, verifica se o parametro t é 1 (se for 1 quer dizer que é uma pasta e se for 0 é um arquivo)
        if list_files[key]['t'] == 1:
            #se a pasta iniciar com '.', não será baixada, pois é uma pasta oculta
            if list_files[key]['a']['n'][0] == '.':
                continue
            #quando uma pasta é achada, é chamada a mesma função novamente para fazer o download dos arquivos dentro da pasta
            #list_files[key]['h'] é o codigo
            __download_rec(obj_mega, list_files[key]['h'], path.join(path_to, list_files[key]['a']['n']))
        #caso for um arquivo, será baixado
        elif list_files[key]['t'] == 0:
            #é verificado se esse arquivo ainda não foi baixado, se foi, continua
            if path.isfile(path.join(path_to, list_files[key]['a']['n'])):
                continue

            #se a pasta de destino não existe, é criada
            if not path.isdir(path_to):
                path.mkdirs(path_to)

            #por fim, baixa o arquivo e coloca na pasta de destino
            print("download:", list_files[key]['a']['n'])
            obj_mega.download((key, list_files[key]), dest_path=path_to)

#testes:
if __name__ == "__main__":
    m = login("imri.data@gmail.com", "mydata_imri01")
    a = get_code(m, "images_out")
    if a is not None:
        __download_rec(m, a, path.join(path.resource, "images_out"))