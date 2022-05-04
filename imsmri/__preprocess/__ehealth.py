from .. import __path as path
from .. import __files as files
from .. import __json as json
from .. import __images as images
import os

#obtem o nome do arquivo no formado 'NOMEBANCO_NUM.FORMATO', caso já exista, ele incrementa o NUM até que não tenha outro igual
def get_name(data, form, num=0):
    path_out = path.join(path.files_out, data["dataset"].upper()+"_"+data["patient_code"]+"_"+str(num)+"."+form)
    if not path.isdir(path.files_out):
        path.mkdirs(path.files_out)

    if files.find(path.dirname(path_out), path.lastname(path_out)) is not None:
        return get_name(data, form, num=num+1)
    return path_out

#quando encontra o diretório das imagens, ele busca todas as imagens da mesma pasta e faz uma copia das imagens
#para a mesma pasta images_out dos outros bancos de dados
def find_all(data, path_files, form, dim):
    arqs = os.listdir(path_files)
    for arq in arqs:
        if ".plq" in arq:
            continue

        name = arq.split(".")[0]

        for proc in arqs:
            #caso tenha o arquivo com formato .plq, quer dizer que essa imagem possui o problema e pode ser classificada como doente
            if not ".plq" in proc or not name in proc:
                continue

            fullname = get_name(data, form)
            img = images.read(path.join(path_files, arq))
            img = images.rotate(img, -90)
            #removendo letras dos cantos da imagem
            img[:50,:] = 0
            img[-50:,:] = 0
            img[:70,:70] = 0
            img[-70:,:70] = 0
            img[:70,-70:] = 0
            img[-70:,-70:] = 0
            images.save(fullname, img, tam=dim)

            js = json.__file_data(data)
            js["view"] = "axial"
            js["weighting"] = "T2"
            js["local_path"] = path.lastname(fullname)
            json.__final_json.insert(js)
            break

def process(data, form, dim):
    #verifica a existencia do arquivo descompactado
    filename = data["filename"].split(".")[0]
    if not path.isdir(path.join(path.files_unzip, data["dataset"], filename)):
        raise Exception(path.join(path.files_unzip, data["dataset"], filename)+": nonexistent directory")

    path_ehealth = path.join(path.files_unzip, data["dataset"], filename)

    #verificar se esse paciente já foi preprocessado
    if json.__final_json.ispatient(data["dataset"], data["patient_code"]):
        json.__final_json.delete_exam(data["dataset"], data["patient_code"])

    all_dirs = []

    #procura por todos os subdiretórios buscando os arquivos em que estão as imagens
    for dirname, drs, fls in os.walk(path_ehealth):
        if path.lastname(dirname) != data["patient_code"]:
            continue

        for dr, dirnames, filenames in os.walk(dirname):
            if dr in all_dirs:
                continue

            for f_name in filenames:
                #caso encontre, chama a função find_all
                if ".plq" in f_name:
                    all_dirs.append(dr)
                    find_all(data, dr, form, dim)
                    break