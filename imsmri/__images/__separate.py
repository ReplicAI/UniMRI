from . import __get_info
from ..api import mega
from .. import __path as path
from .. import __json as json
import shutil

'''
keys:
"type", "key" definidas no arquivo __get_info
"local_path" definida no arquivo preprocess/__to_slice
'''

#path padrão das imagens
__path_json = path.files_out

#cria as pastas training/validation/test no mesmo diretorio das imagens e move as imagens para lá
#a variavel "used_as" é criada aqui e usada no load das imagens
#mesmo que as imagens já estejam separadas em pastas, a função recoloca as imagens onde deve, fazendo com que
#se possa separar as imagens diversas vezes
def _generate_folders(lista_training, lista_validation, lista_test):
    global __path_json

    #abre o json das imagens
    myjson = json.__final_json__.final_json()
    myjson.load(path_json=__path_json)
    #lista todos os metadados e o local onde se encontra as imagens no disco
    all_data = myjson.data()

    #itera sobre a lista de dados de treinamento
    for file in lista_training:
        #se a pasta training não existe, é criada
        if not path.isdir(path.join(__path_json, "training")):
            path.mkdirs(path.join(__path_json, "training"))

        #aqui é usada a chave (key) e o tipo (type) definidos na função __get_info() do arquivo __get_info
        data_img = all_data[file["type"]][file["key"]]
        #movemos a imagem para a pasta criada (ou existente)
        shutil.move(path.join(__path_json, data_img["local_path"]),
                    path.join(__path_json, "training", path.lastname(data_img["local_path"])))
        #atualizamos o diretório relativo da imagem no json
        data_img["local_path"] = path.join("training", path.lastname(data_img["local_path"]))
        #criamos a variavel used_as e definimos que tipo de dado é (nesse caso é training)
        data_img["used_as"] = "training"
        #salvamos o json
        myjson.save()

    #mesmo caso do training, mas para validation
    for file in lista_validation:
        if not path.isdir(path.join(__path_json, "validation")):
            path.mkdirs(path.join(__path_json, "validation"))

        data_img = all_data[file["type"]][file["key"]]
        shutil.move(path.join(__path_json, data_img["local_path"]),
                    path.join(__path_json, "validation", path.lastname(data_img["local_path"])))
        data_img["local_path"] = path.join("validation", path.lastname(data_img["local_path"]))
        data_img["used_as"] = "validation"
        myjson.save()

    #mesmo caso do training e validation, mas para test
    for file in lista_test:
        if not path.isdir(path.join(__path_json, "test")):
            path.mkdirs(path.join(__path_json, "test"))

        data_img = all_data[file["type"]][file["key"]]
        shutil.move(path.join(__path_json, data_img["local_path"]),
                    path.join(__path_json, "test", path.lastname(data_img["local_path"])))
        data_img["local_path"] = path.join("test", path.lastname(data_img["local_path"]))
        data_img["used_as"] = "test"
        myjson.save()

    #retorna as listas (não necessario, mas pode ter utilidade futuramente)
    return lista_training, lista_validation, lista_test

#junta as duas lista em uma só e de forma intercaladas entre os elementos: [l1[0], l2[0], l1[1], l2[1], ...]
def _sep(list1, list2):
    lista = []

    itr = [iter(list1), iter(list2)]

    i, end = 0, [0, 0]
    while sum(end) < 2:
        i = 1 if i == 0 else 0

        try:
            lista.append(next(itr[i]))
        except StopIteration:
            end[i] = 1

        i = 1 if i == 0 else 0

        try:
            lista.append(next(itr[i]))
        except StopIteration:
            end[i] = 1

        i = 1 if i == 0 else 0

    return lista

#aqui é feita a divisão dos dados em três listas principais, os dados saudaveis, doentes que são treinamento e doentes que são dados de teste
#e são criadas mais três listas que armazenarão a divisão dos dados
def _put_in_list(info, qtd_training, qtd_validation, qtd_test):
    saudaveis = [v for v in info["files_training"] if not v["MS"]]
    doentes_training = [v for v in info["files_training"] if v["MS"]]
    doentes_test = [v for v in info["files_test"]]

    #listas a serem preenchidas
    lista_training = []
    lista_validation = []
    lista_test = []

    #teste só pode ser teste
    lista_test.extend(doentes_test)
    #verifica o que falta dos dados de teste a ser preenchido (se faltar)
    qtd_test = qtd_test - len(lista_test) if (qtd_test - len(lista_test)) >= 0 else 0

    #_sep: gera um lista de saudaveis e doentes de forma em que os dados fiquem intercalados entre si
    #para que cada separação entre treino/validação/teste tenha imagens tanto de doentes como de saudaveis
    full_list = _sep(saudaveis, doentes_training)
    itr = iter(full_list)

    #itera sobre todos os dados disponiveis
    while qtd_training > 0 or qtd_validation > 0 or qtd_test > 0:
        #distribui as imagens entre as três listas (treino/validação/teste)
        try:
            if qtd_training > 0:
                lista_training.append(next(itr))
                qtd_training -= 1
        
            if qtd_validation > 0:
                lista_validation.append(next(itr))
                qtd_validation -= 1

            if qtd_test > 0:
                lista_test.append(next(itr))
                qtd_test -= 1

        except StopIteration:
            break

    #chama a função para a criação das três pastas onde os dados serão colocados, pastas training, validation e test
    return _generate_folders(lista_training, lista_validation, lista_test)

#Separa os dados entre treinamento, validação e teste.
def separate(training=None, validation=None, test=None, path_files=None, from_mega=False):
    global __path_json
    #faz verificações sobre os parametros. Os parametros para separar os dados (training, validation, test) tem que ser None, 0 <= x <= 1
    if training is not None and not 0.0 <= training <= 1.0:
        raise Exception("images -> separate: Values ​​out of range (0 to 1)")
    elif validation is not None and not 0.0 <= validation <= 1.0:
        raise Exception("images -> separate: Values ​​out of range (0 to 1)")
    elif test is not None and not 0.0 <= test <= 1.0:
        raise Exception("images -> separate: Values ​​out of range (0 to 1)")

    #esse vetor serve para auxiliar na hora de saber quais variaveis foram definidas pelo usuario
    #todos os valores que foram recebidos como None, ficam -1
    #e como já sabemos que os valores estão de 0 a 1, não haverá problemas
    values = []
    values.append(training if training is not None else -1)
    values.append(validation if validation is not None else -1)
    values.append(test if test is not None else -1)

    #se os 3 valores recebidos forem nulos, quer dizer que o usuario não definiu nenhum
    #então, valores padrões são definidos
    if sum(values) == -3:
        training = 0.5
        validation = 0.25
        test = 0.25
    else:
        #a soma dos três parametros devem resultar em, no maximo, 1.
        #então, aqui é calculado: 1 menos a soma de todos os valores que o usuario definiu
        #e esse resultado é o que falta para completar 100% (1)
        restante = 1.0 - sum([v for v in values if v >= 0])

        #se não resta nada, então o usuario definiu os três valores (training, validation, test) corretamente
        if restante <= 0.0:
            #mas o usuario pode ter colocado um só parametro como 1. Então aqui é feita uma verificação para ver quais foram definidos
            training = values[0] if values[0] != -1 else 0
            validation = values[1] if values[1] != -1 else 0
            test = values[2] if values[2] != -1 else 0
        else:
            #se ainda resta algo para ser definido, o algoritmo define automaticamente
            #aqui, é verificado se a soma dos não definidos pelo usuario é 2
            #se dois valores não foram definidos pelo usuario, então o restante é dividido entre esses dois valores faltantes
            #se só um não foi definido, então o restante todo vai para essa variavel
            restante = restante / 2 if sum([1 for v in values if v == -1]) == 2 else restante
            #coloca os valores nos campos faltantes (-1)
            for i in range(len(values)):
                if values[i] == -1:
                    values[i] = restante
                
            training, validation, test = values

    #verifica se a soma das 3 variaveis é maior que 1, se for, o usuario definiu algo errado
    if sum([training, validation, test]) > 1.0:
        raise Exception("Sum of values ​​> 1.0")

    #essa variavel é global, pois ela será acessada nas outras funções também
    #ela contém o diretório das imagens de saida e do json final
    #path.files_out é o diretório padrão de saida das imagens, definida pelo usuario na função load e no subpacote path no __init__
    __path_json = path.files_out

    #é aqui que os dados são baixados do mega. quando o parametro from_mega é True, é buscado os arquivos no mega e faz o download
    #se não foi possivel encontrar o arquivo, uma exceção é gerada
    if from_mega:
        resp = mega.__download_images_out()
        if not resp:
            raise Exception("Mega Downloader: 'images_out.zip' file not found!")

        #quando os dados são baixados, __path_json recebe o novo diretório dos dados baixados
        __path_json = path.join(path.resource, "images_out")
    elif path_files is not None:
        #path_files é definido pelo usuario manualmente, esse é o caso da pasta images_out estar em algum outro lugar do pc
        __path_json = path_files

    #é obrigatório ter o json final na pasta images_out, se não tiver, gerará uma exceção
    if not path.isfile(path.join(__path_json, "final_json.json")):
        raise Exception("Images get_info: '"+str(path.join(__path_json, "final_json.json"))+"' file not found!")

    #a partir daqui, as variaveis training, validation e test contém a proporção de dados a ser separado

    #obtem as informações das imagens (suas quantidades)
    info = __get_info.get_info(paths=__path_json)
    #define o total de imagens
    total = info["training"] + info["test"]
    #aqui a % é usada para determinar a quantidade de dados de treinameto que serão usadas
    qtd_training = int(training * total)
    
    #se a quantidade de dados de treinamento escolhida for maior do que a quantidade de exames de treinamento disponivel
    #a quantidade volta para o limite, pois os dados de treinamento não podem ser os dados de teste (pois não tem rotulos)
    if qtd_training > info["training"]:
        qtd_training = info["training"]

    #verifica quantos dados de treinamento sobraram
    disp = info["training"] - qtd_training
    qtd_validation = int(validation * total)

    #verifica se a quantidade que sobrou de dados de treinamento é suficiente para suprir os dados de validação
    #se não for, a quantidade de validação volta pro limite disponivel
    if qtd_validation > disp:
        qtd_validation = disp

    #os dados de testes ficam com o que sobrou dos outros dois tipos de dados
    qtd_test = total - (qtd_training + qtd_validation)

    #as variaveis qtd_training, qtd_validation, qtd_test já contém as quantidades de dados de cada tipo
    #a serem usados e separados
    return _put_in_list(info, qtd_training, qtd_validation, qtd_test)