import os
from ... import __path as path

#recebe um diretorio ex: "/dataset/pre" e retorna o código da pasta no mega (caso exista)
#o mega usa um sistema de código para anexar arquivos e pastas, e não um diretório em string
def get_code(obj_mega, path_rec, t_a=0):
    try:
        v = obj_mega.find_path_descriptor(path_rec)
        return v
    except:
        if t_a >= 3:
            #as vezes a api mega gera uma exceção não sistematica e que geralmente, tentar mais de uma vez, resolve o problema
            #por isso, é feita 3 tentativas antes de gerar esse erro
            raise Exception("[ERROR] Try again in 5 minutes.")
        return get_code(obj_mega, path_rec, t_a=t_a+1)

#procura um arquivo dentro de um diretorio do mega. Caso ache, ele retorna um json com todas as infos do arquivo
def find_file(obj_mega, path_file):
    #obtem o codigo da pasta em que o arquivo está
    code = get_code(obj_mega, path.dirname(path_file))
    #se não existir esse diretorio, o arquivo não existe também, então retorna None
    if code is None:
        return None

    #get_files_in_node lista todos os arquivos de um determinado diretório
    files = obj_mega.get_files_in_node(code)
    #percorremos todos os arquivos até achar o arquivo que procuramos (caso exista)
    for i in files:
        #files é um dicionario de dicionarios (a api do mega trabalha assim), formato: files = {'codigo do arquivo': {'h': 'codigo do arquivo', 'a':{'n': 'nome do arquivo'}}} (tem mais infos, mas essas são usadas aqui)
        #o iterador i é o proprio codigo do arquivo (o mesmo do files[i]['h'])
        if files[i]['a']['n'] == path.lastname(path_file):
            return files[i]

    return None

#Essa função recebe um path e o cria caso não exista, se já existe, retorna o código do diretório
def make_dir(obj_mega, path_dir):
    #verifica se alguma parte do path existe, ex: "/dataset/pre/miccai08"
    #ele verifica se existe "/dataset/pre/miccai08", dps: "/dataset/pre", dps: "/dataset"
    #caso encontre um existente, ele retorna o codigo da pasta e o restante do path a ser criado
    def exists():
        path_s, rest = path_dir, ""
        while len(path_s) > 1:
            #no inicio, path_s tem o path completo, caso exista, o get_code retorna o codigo
            #e ai retornaria o codigo e o restante do path a ser criado (no caso, se o path completo já existir, rest é vazio)
            res = get_code(obj_mega, path_s)
            if res is not None:
                return res, rest
            
            #caso não exista, rest recebe o nome da ultima pasta de path_s, fazendo isso até achar um path existente
            #se não existir nenhum, retornará None depois desse while
            rest = path.join(path.lastname(path_s), rest) if rest != "" else path.lastname(path_s)
            #a função dirname retira o nome da ultima pasta
            path_s = path.dirname(path_s)

        return None

    #if o path recebido pela função make_dir for vazio ou uma barra, retorna o codigo diretamente
    if path_dir == "" or path_dir == "/":
        return get_code(obj_mega, path_dir)

    #chama a função exists, se for None, o path inteiro não existe, então criará esse diretório e retornará seu codigo
    res = exists()
    if res is None:
        out = obj_mega.create_folder(path_dir)
        #o retorno da função create_folder é um dicionario em que seus indexadores são os nomes das pastas do diretorio e o conteudo é o codigo da pasta
        #no caso, retorna o conteudo (o codigo) do indexador da ultima pasta do diretório
        return out[path.lastname(path_dir)]
    elif res[1] == "":
        #se 'res' é diferente de None, e o path inteiro existe, retorna seu codigo
        return res[0]

    #aqui é a ultima etapa, caso somente parte do path existir, então a outra parte será criada dentro da já existente
    out = obj_mega.create_folder(res[1], dest=res[0])
    return out[path.lastname(path_dir)]