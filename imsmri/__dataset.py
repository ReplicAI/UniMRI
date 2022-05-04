from . import __path as path
from . import __json as json
from . import __files as files
from .api import mega
from . import __preprocess
import os, shutil

#essas funções (download,unzip,change_extensions,upload) são funções em que o usuário não tem controle sobre
#diferente das funções de pré-processamento em que pode ser retiradas pelo usuário
#essa variavel armazena as funções padrões que sempre serão utilizadas
__functions__defaults = ["download", "unzip", "change_extensions", "upload"]

#carrega os diretórios para uso no pacote (usado no pre-processamento)
def load(path_datasets, path_pre, path_unzip_data=path.files_unzip, path_mega_source=path.mega_source):
    #reseta todos os paths, caso já tenha sido definido
    path.__reset()
    #verifica se os paths recebidos pelo usuario são validos, existentes e absolutos
    path_z, path_p = path.verify(path_datasets), path.verify(path_pre)
    #se não for, gerará exceções
    if not path_z:
        raise Exception(path_datasets+": non-existent directory. Only full directory")
    elif not path_p:
        raise Exception(path_pre+": non-existent directory. Only full directory")

    #verifica se o parametro opcional foi usado, se sim, verifica se ele é valido, existente e absoluto
    if path_unzip_data != path.files_unzip:
        path_u = path.verify(path_unzip_data)
        if not path_u:
            raise Exception(path_unzip_data+": non-existent directory. Only full directory")
        path.files_unzip = path_u

    #serve para mudar a pasta onde os dados são colocados no mega (futuramente seria melhor retirar essa possiblidade para evitar maiores problemas)
    if path_mega_source != path.mega_source:
        path.mega_source = path_mega_source

    #caso todos os paths sejam validos, atualiza os paths no subpacote __path (gerencia todos os paths)
    path.files_zip = path_z
    path.files_pre = path_p
    path.files_out = path.join(path.files_pre, path.files_out)

    #quando os diretórios são definidos, é criado o json principal contendo todos os metadados de todos os exames que esse pacote possui informação
    return json.__create()

#verifica se um paciente já existe no json final (json gerado depois do pre-processamento dos dados)
#essa função é usada para não pre-processar o mesmo exame duas vezes (exceto se o parametro replace na função run seja True)
def check_patient_existence(data):
    if json.__final_json.ispatient(data["dataset"], data["patient_code"]):
        return True
    return False

#quando o parametro init é False na função run, um arquivo temp é criado informando o progresso do pré-processamento
#caso o programa seja fechado no meio de um pré-processamento, esse arquivo temp é usado para voltar de onde parou
#essa função 'check' serve para verificar se a sequencia é a mesma sequencia salva na arquivo temp
#se não for, não tem como voltar de onde parou, gerando assim, uma exceção
def check(funcs):
    #se o arquivo temp não existe, não há problemas, então retorna True
    if not path.isfile(path.temp_file):
        return True

    with open(path.temp_file, "r") as temp:
        tp = json.__load(temp)
        #se a quantidade de funções contidas no arquivo temp for diferente das funções selecionadas, gerará uma exceção
        if len(tp["funcs_name"]) != len(funcs):
            raise Exception("Sequence not compatible. If you want to change the sequence, use the init parameter as True to restart!")
        
        for name1, name2 in zip(tp["funcs_name"], funcs):
            if name1[0] is None and name2 is None:
                continue

            #verifica se os nomes das funções são diferentes, se forem, gerará uma exceção
            if name1[0] != name2.__name__:
                raise Exception("Sequence not compatible. If you want to change the sequence, use the init parameter as True to restart!")

#salva o arquivo temp sempre depois de terminar alguma etapa do pré-processamento
def save(i, funcs):
    with open(path.temp_file, "w") as temp:
        #salva o nome das funções e se já foram concluidas, ex: ['skull_strip', True]
        #a função download/upload podem ser None se o usuario não for baixar/enviar os dados pro mega
        #o 'i' informa em qual exame o processamento parou
        json.__dump({
            "funcs_name": [[v[0].__name__, v[1]] if v[0] != None else [v[0], v[1]] for v in funcs],
            "i": i
        }, temp)

#como o nome sugere, essa função le o arquivo temp e retorna as informações
def load_save():
    #caso não exista, o pre-processamento parte do inicio
    if not path.isfile(path.temp_file):
        return None, 0

    with open(path.temp_file, "r") as temp:
        tp = json.__load(temp)
        return tp["funcs_name"], tp["i"]

#run começa o pre-processamento dos dados
def run(funcs, all_data, to, init, replace, continue_from_mega):
    global __functions__defaults
    #carregar funções
    all_funcs = []
    
    #se o parametro opcional download for True, a função de download da api mega é colocada na lista all_funcs
    if funcs["download"]:
        #se essa variavel for None, o usuario não se logou no mega, então não tem como fazer o download
        if mega.__downloader is None:
            raise Exception("API Mega: No user logged in!")

        all_funcs.append(mega.__download)
    else:
        #caso não precise fazer o download, um valor nulo é colocado na lista
        all_funcs.append(None)

    #a lista de funções se extende para as funções padrões como unzip e change_extensions
    all_funcs.extend([files.__unzip, files.__change_extensions])
    #e agora se extende para as funções definidas pelo usuario
    all_funcs.extend(funcs["funcs"])

    #aqui é o mesmo do download, se precisar fazer o upload dos dados, e adiocionado a lista de funções
    if funcs["upload"]:
        if mega.__uploader is None:
            raise Exception("API Mega: No user logged in!")

        all_funcs.append(mega.__upload)
    else:
        all_funcs.append(None)

    #verificar funções duplicadas (download, unzip, change extensions, upload)
    #se houver alguma função definida mais de uma vez, gerará uma exceção
    for c in __functions__defaults:
        #soma todas as vezes em que cada função aparece, se a soma for maior que 1, quer dizer que apareceu mais de uma vez a mesma função
        if sum([1 if c in v.__name__ else 0 for v in all_funcs if v is not None]) > 1:
            raise Exception("Invalid Sequence. Do not use internal functions (starting with '__') in the sequence")

    #se o parametro init for True, o arquivo temp é removido (caso exista)
    #caso for False, chama a função check para verificar se a sequencia atual é a mesma definida no arquivo temp
    if init:
        if path.isfile(path.temp_file):
            path.remove(path.temp_file)
    else:
        check(all_funcs)

    #lê o arquivo temp (caso exista) para saber de onde iniciar
    list_funcs, ini = load_save()
    #to: define quantos exames serão pré-processados, se 'to' ultrapassar a quantidade de dados selecionados, receberá o valor limite (preprocessa até o final)
    to = ini + to if to != -1 else len(all_data)
    to = len(all_data) if to > len(all_data) else to

    #list_funcs é usado para chamar as funções definidas em sequence, caso for None, quer dizer que ta iniciando do inicio e não do arquivo temp
    if list_funcs is None:
        #recebe as funções da lista all_funcs e False (False indica que a função ainda não foi concluida (no inicio nenhuma função foi concluida :D))
        list_funcs = [[v, False] for v in all_funcs]
    else:
        #mais uma verificação (talvez desnecessaria, mas verificar sempre é importante)
        #se a quantidade de funções definidas em list_funcs for diferente de all_funcs, uma exceção será gerada
        if len(list_funcs) != len(all_funcs):
            raise Exception("Sequence not compatible. If you want to change the sequence, use the init parameter as True to restart!")

        #recebe as funções da lista all_funcs (list_funcs tem as funções em string(lidas do arquivo temp), aqui a lista recebe as funções reais)
        for lf, af in zip(list_funcs, all_funcs):
            if lf[0] is None and af is None:
                continue

            #recebe as funções, mas aqui não recebe False, pois o valor True/False vem do arquivo temp, para poder voltar de onde parou
            lf[0] = af

    #se a pasta onde os arquivos são descompactados existir, será removido para evitar problemas de arquivos corrompidos
    #toda vez que um exame é pre-processado, ele é descompactado novamente
    if path.isdir(path.files_unzip):
        shutil.rmtree(path.files_unzip)

    #caso o continue_from_mega for True, será baixado as imagens do mega para continuar de onde parou
    #essa função só funciona quando se usa o pré_processamento to_slice e upa os dados pro mega usando a função upload_images_out da api mega
    if continue_from_mega:
        if mega.__downloader is None:
            raise Exception("API Mega: No user logged in!")

        print("Downloading data from MEGA...")
        #chama a função de download das imagens
        mega.__download_images_out(path_to=path.files_pre)

    #essa lista serve para, caso o exame já tenha sido pré-processado, possa ser adicionado mais um elemento e o for continuar
    #só é usado quando replace é False
    perc_list = list(range(ini, to))
    #para cada iteração desse for, um exame é pre-processado
    for d in perc_list:
        #informa os detalhes do exame que está sendo pré-processado
        print("[{0}/{1}] Info: dataset: {2}, patient code: {3}, sex: {4}, age: {5}, ms: {6}, ms_type: {7}, filezip: {8}".format(
            d+1, to,
            all_data[d]["dataset"],
            all_data[d]["patient_code"],
            all_data[d]["sex"],
            all_data[d]["age"],
            all_data[d]["MS"],
            all_data[d]["ms_type"],
            all_data[d]["filename"]
        ))

        #verifica se o exame já foi pré-processado (somente se usar a função to_slice)
        #se não usar, essa função sempre retornará False
        if check_patient_existence(all_data[d]):
            #se o replace for True, somente informa que esse exame ja foi pré-processado, mas preprocessa novamente
            if replace:
                print("NOTE: Patient has already been pre-processed.")
            else:
                print("NOTE: Patient has already been pre-processed. Skipping...")
                to += 1
                #se to+1 ainda for menor ou igual a quatidade de dados total, adiciona mais um exame no final da lista para ser pré-processado
                #se não, não faz nada, somente volta o to para o tamanho original
                if to <= len(all_data):
                    perc_list.append(perc_list[-1]+1)
                else:
                    to -= 1

                continue

        #roda todas as funções para esse exame (todas as funções de pré-processamento e manipulação, recebem somente um dicionario com todas as informações do exame)
        for f in list_funcs:
            #se a função ainda não foi executada (f[1] (True ou False)) e a função é diferente de None, executa ela
            if not f[1] and f[0] != None:
                #salva o estado atual no arquivo temp
                save(d, list_funcs)
                #informa o que ta sendo executado
                print("exec:", f[0].__name__.replace("__", ""))
                #chama a função
                f[0](all_data[d])
                #caso a função executada for uma função padrão (que sempre será executada, mesmo que o programa volte de onde parou)
                #ela volta para False, caso for uma função do pre-processamento, vai pra True
                f[1] = True if not "unzip" in f[0].__name__ and not "change_extensions" in f[0].__name__ else False

        #Volta a list_funcs para False para cada função, pois um novo exame será pré-processado
        list_funcs = [[v[0], False] for v in list_funcs]
        #salva o proximo exame
        save(d+1, list_funcs)
        print("Done.\n")

    #quando tudo acabar, essa função apaga os dados descompactados
    if path.isdir(path.files_unzip):
        shutil.rmtree(path.files_unzip)
        
    print("Done!")