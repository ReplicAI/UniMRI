from ... import __json, __files
from ... import __path as path
from .__functions import make_dir, find_file
from .__download import download_images_out
from mega import Mega
import os, shutil

#faz o login no mega, caso a email/senha esteja errada, gerará um exception
def login(email, passwd):
    #mesmo sistema do download
    mm = Mega()
    try:
        obj = mm.login(email, passwd)
        return obj
    except:
        raise Exception("uploader: Invalid Email or Password!")

#As vezes da problema na api, por isso ele tenta upar os dados até três vezes
def _upload(obj_mega, path_file, code, t_a=0):
    try:
        #se o codigo for None, os dados serão upados no diretorio raiz do mega
        if code is None:
            file = obj_mega.upload(path_file)
        else:
            #caso seja especificado, upa o arquivo no diretorio escolhido
            file = obj_mega.upload(path_file, dest=code)
        return file
    except:
        if t_a >= 3:
            raise Exception("[ERROR] Try again in 5 minutes.")
        return _upload(obj_mega, path_file, code, t_a=t_a+1)

#A função que upa algum diretório indicado pro mega
#também não é usada por enquanto, mas futuramente pode ser util
def upload_folder(obj_mega, path_folder):
    #se a pasta não existir, retorna False
    if not path.isdir(path_folder):
        return False

    #caminha por todos os subdiretorios dessa pasta
    all_files = []
    for dirname, dirnames, filenames in os.walk(path_folder):
        #se for uma pasta de cache do python, não é upada :D
        if path.lastname(dirname) == "__pycache__":
            continue

        #lista todos os arquivos internos
        for filename in filenames:
            #se o arquivo existir no mega, não será upado
            find = find_file(obj_mega,
                path.join(path.lastname(path_folder), path.diference(dirname, path_folder), filename))
            if find is not None:
                continue

            #obtem o codigo da pasta, coloca na lista o retorno da função de upload
            #upando assim, o arquivo
            code = make_dir(obj_mega, path.join(path.lastname(path_folder), path.diference(dirname, path_folder)))
            all_files.append(_upload(obj_mega, path.join(dirname, filename), code))

    return all_files

#esse upload é usado e muito importante, ele é o upload que envia e junta os dados da pasta images_out para o mega
#mesmo que ja tenha uma pasta images_out no mega, essa função faz a fusão das duas, não deletando nem uma nem outra, mas juntando-as
def upload_images_out(obj_mega):
    #se não existir o json final no path padrão, retorna False
    if not path.isfile(path.join(path.files_out, __json.__final_json.filename)):
        return False

    #faz o download da pasta existente no mega, para que a fusão seja feita
    resp = download_images_out(obj_mega)

    #se não tem o arquivo images_out.zip no mega, ele simplesmente compacta e upa a pasta para o mega
    if not resp:
        #se existe o arquivo images_out.zip baixado, é excluido
        if path.isfile(path.join(path.resource, "images_out.zip")):
            path.remove(path.join(path.resource, "images_out.zip"))

        #upa a pasta images_out e envia o arquivo para a pasta de recursos
        __files.__zip(path.files_out, path.join(path.resource, "images_out"))
        #se deu tudo certo com a compressão, faz o upload do arquivo pro mega
        if path.isfile(path.join(path.resource, "images_out.zip")):
            _upload(obj_mega, path.join(path.resource, "images_out.zip"), None)
            return True
        return False

    #caso exista um arquivo no mega, já foi baixado
    #aqui é verificado se a pasta images_out baixada em o json, se não tiver, uma exceção é gerada
    if not path.isfile(path.join(path.resource, "images_out", __json.__final_json.filename)):
        raise Exception("final_json: '"+str(path.join(path.resource, "images_out", __json.__final_json.filename))+"' not found!")

    #abre o json baixado do mega
    temp_json = __json.__final_json__.final_json()
    #se retornar False, o json está vazio, então uma exceção é gerada
    if not temp_json.load(path_json=path.join(path.resource, "images_out")):
        raise Exception("Error opening json file:", path.join(path.resource, "images_out", __json.__final_json.filename))

    xlist = []
    for dirname, dirnames, filenames in os.walk(path.files_out):
        #se for uma pasta __pycache__ é ignorada
        if path.lastname(dirname) == "__pycache__":
            continue

        #anda por todos os arquivos dentro da pasta images_out local
        for filename in filenames:
            #se o arquivo for o proprio json, então continua
            if __json.__final_json.filename in filename:
                continue

            #verifica se esse exame já entá dentro do json baixado do mega
            info = filename.split("_")
            if len(info) < 3:
                continue

            info = info[:-1]
            info = [info[0], '_'.join(info[1:]) if len(info[1:]) > 1 else info[1]]

            #se esse exame ja existe, então continua
            if temp_json.ispatient(info[0], info[1]) and not [info[0], info[1]] in xlist:
                continue

            data = __json.__final_json.get_patient(filename)
            if not data:
                continue

            if not [info[0], info[1]] in xlist:
                xlist.append([info[0], info[1]])

            #se não existe esse arquivo no mega, então esse arquivo é copiado para a pasta que será upada
            shutil.copyfile(
                path.join(dirname, filename),
                path.join(path.resource, "images_out", path.diference(dirname, path.files_out), filename))
            #insere esse dado no json do mega
            temp_json.insert(data)

    #se o arquivo zipado existir, é deletado
    if path.isfile(path.join(path.resource, "images_out.zip")):
        path.remove(path.join(path.resource, "images_out.zip"))

    #se a pasta baixada do mega não existir, algo de errado não está certo :D
    if not path.isdir(path.join(path.resource, "images_out")):
        return False

    #compacta a pasta images_out com a fusão dos arquivos
    __files.__zip(path.join(path.resource, "images_out"), path.join(path.resource, "images_out"))

    #se deu tudo certo, se o arquivo zipado existir, o programa continua
    if not path.isfile(path.join(path.resource, "images_out.zip")):
        return False
    
    #upa o arquivo zip pro mega
    _upload(obj_mega, path.join(path.resource, "images_out.zip"), None)
    #apaga o arquivo que já estava no mega (é apagado depois do outro ser upado, para não dar problemas)
    obj_mega.destroy(resp['h'])
    return True

#Essa função faz o upload dos dados pré processados pro mega
def upload(obj_mega, data, folder):
    all_files = []
    #verifica cada path pre para upar cada imagen 3D pro meg
    for mod in ["path_T1_pre", "path_T2_pre", "path_FLAIR_pre", "path_lesion_pre", "path_data"]:
        if mod in data.keys() and path.isfile(data[mod]):            
            dir_file = path.join(folder, data["original_path"], path.lastname(data[mod]))
            resp = find_file(obj_mega, dir_file)

            #cria a pasta para upar os dados
            code = make_dir(obj_mega, path.join(folder, data["original_path"]))
            #upa o arquivo
            file = _upload(obj_mega, data[mod], code)
            all_files.append(file)

            #apagando arquivo anterior caso exista
            if resp is not None:
                obj_mega.destroy(resp['h'])

    return all_files