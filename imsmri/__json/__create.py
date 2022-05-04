from . import dataset
from .. import __path as path
import json

__exclusions = ["oasis", "ehealth"]

#Essa função define o tipo dos dados ("training"/"test") e cria os diretórios onde serão salvas as imagens pré-processadas. 
def _add_paths(databases):
    training = databases['training']
    test = databases['test']

    #cria a chave datatype identificando o tipo dos dados originalmente
    for data_dict in training:
        data_dict["datatype"] = "training"

    for data_dict in test:
        data_dict["datatype"] = "test"

    #coloca todos os dados em uma unica lista
    full_data = []
    full_data.extend(training)
    full_data.extend(test)

    for data_dict in full_data:
        global __exclusions
        #Se for o dataset oasis, ele criará os paths na função __include__oasis
        #Se for o eheath, ele simplesmente não cria, pois o ehealth já tem suas imagens pré-processadas
        if data_dict["dataset"] in __exclusions:
            continue
        
        #original
        #esse path é usado para criar a estrutura de pastas dentro do mega
        data_dict["original_path"] = path.dirname(data_dict["path_T1"])

        #pre - diretórios para onde os dados pré-processados irão
        #lembrando que path.files_pre é definido pelo usuario na função load
        data_dict["path_T1_pre"] = path.join(path.files_pre, data_dict["path_T1"])
        data_dict["path_T2_pre"] = path.join(path.files_pre, data_dict["path_T2"])
        data_dict["path_FLAIR_pre"] = path.join(path.files_pre, data_dict["path_FLAIR"])
        data_dict["path_lesion_pre"] = path.join(path.files_pre, data_dict["path_lesion"]) if data_dict["path_lesion"] != "" else ""

        #unzip
        #o diretório para onde os dados descomprimidos irão
        #não depende do usuario
        data_dict["path_T1"] = path.join(path.files_unzip, data_dict["path_T1"])
        data_dict["path_T2"] = path.join(path.files_unzip, data_dict["path_T2"])
        data_dict["path_FLAIR"] = path.join(path.files_unzip, data_dict["path_FLAIR"])
        data_dict["path_PD"] = path.join(path.files_unzip, data_dict["path_PD"]) if data_dict["path_PD"] != "" else ""
        data_dict["path_T1GADO"] = path.join(path.files_unzip, data_dict["path_T1GADO"]) if data_dict["path_T1GADO"] != "" else ""
        data_dict["path_lesion"] = path.join(path.files_unzip, data_dict["path_lesion"]) if data_dict["path_lesion"] != "" else ""

        #liubliana e isbi são casos especiais em que o local da mascara de lesão é diferente do local do restante dos dados
        #então, o local de destino (pre) da mascara tem que ser alterado para que todos os dados fiquem juntos
        if data_dict["dataset"] == "liubliana" and data_dict["path_lesion_pre"] != "":
            sep = data_dict["path_lesion_pre"].split("/")
            #adiciona 'raw' ao path da mascara
            last, sep[-1] = sep[-1], "raw"
            sep.append(last)
            data_dict["path_lesion_pre"] = path.join(*sep)
            data_dict["path_lesion_pre"] = "/"+data_dict["path_lesion_pre"] if data_dict["path_lesion_pre"][0] != "/" else data_dict["path_lesion_pre"]
        
        if data_dict["dataset"] == "isbi" and data_dict["path_lesion_pre"] != "":
            sep = data_dict["path_lesion_pre"].split("/")
            #troca a pasta 'masks' por 'orig' da mascara, para que quando for pré-processada, ela fique junto com os outros dados
            sep[-2] = "orig" if sep[-2] == "masks" else sep[-2]
            data_dict["path_lesion_pre"] = path.join(*sep)
            data_dict["path_lesion_pre"] = "/"+data_dict["path_lesion_pre"] if data_dict["path_lesion_pre"][0] != "/" else data_dict["path_lesion_pre"]

#Cria o arquivo json principal e imutável.
def _make_file(databases):
    #salva o json
    with open(path.json_file, "w") as f:
        json.dump(databases, f)

#Essa função cria o json principal onde contém todas as informações de todos os bancos de dados usados
def create():
    #cria uma lista com as informações de todos os bancos de dados que o pacote tem suporte
    dbs = []
    dbs.append(dataset.isbi.get())
    dbs.append(dataset.miccai08.get())
    dbs.append(dataset.miccai16.get())
    dbs.append(dataset.liubliana.get())
    dbs.append(dataset.kirby.get())
    dbs.append(dataset.oasis.get())
    dbs.append(dataset.ehealth.get())

    #cria a estrutura para ser salvo em json na proxima função
    DATABASE = {
        "training": [],
        "test": []
    }

    #junta todos os bancos de dados em um dicionario
    for db in dbs:
        #training
        for data in db["training"]:
            DATABASE["training"].append(data)

        #test
        for data in db["test"]:
            DATABASE["test"].append(data)

    #adiciona os diretorios que o usuario definiu (onde os dados estão)
    _add_paths(DATABASE)
    #cria o arquivo json no disco
    _make_file(DATABASE)
    #retorna o dicionario
    return DATABASE