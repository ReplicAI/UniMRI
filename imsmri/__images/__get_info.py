from .. import __path as path
from .. import __json as json
import os

#Essa função abre o json gerado pelo pré processamento to_slice e retorna um json de informações sobre as imagens
#infos como: quantidade de imagens treinamento/teste, doentes/saudaveis, etc.
def get_info(paths=None):
    info = {
        "training": 0,
        "test": 0,
        "healthy": 0,
        "MS": 0,
        "files_training": [],
        "files_test": []
    }

    #cria uma instancia da classe final_json (usada para manipular o json gerado pelo pre-processamento to_slice)
    #com isso, é possivel carregar todas as imagens e seus diretorios, assim como os metadados dos exames
    myjson = json.__final_json__.final_json()
    myjson.load(path_json=paths)
    full_data = myjson.data()

    #esse 'for' itera sobre todos os dados de treinamento
    for keys in full_data["training"]:
        #a cada exame, 1 é adicionado a variavel info["training"] para saber o total de exames do tipo treinamento
        info["training"] += 1
        #acrescenta o tipo, a key e o estado desse exame a lista info["files_training"] para ser usado posteriormente na separação dos dados
        info["files_training"].append({"type": "training", "key": keys, "MS": full_data["training"][keys]["MS"]})
        #salva a quantidade de dados que são doentes e saudaveis
        if full_data["training"][keys]["MS"] == "True":
            info["MS"] += 1
        else:
            info["healthy"] += 1

    #esse 'for' se comporta da mesma maneira que o 'for' de treinamento
    for keys in full_data["test"]:
        info["test"] += 1
        info["files_test"].append({"type": "test", "key": keys, "MS": full_data["training"][keys]["MS"]})
        if full_data["test"][keys]["MS"] == "True":
            info["MS"] += 1
        else:
            info["healthy"] += 1

    #retorna todas as informações dos dados carregados
    return info