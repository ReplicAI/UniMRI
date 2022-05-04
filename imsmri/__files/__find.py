from .. import __path as path
import os

#Procura um arquivo em algum diretório específico com possibilidade de recursão por todos os subdiretórios
def find(path_from, filename, sub_directory):
    #se não for um diretório retorna None
    if not path.isdir(path_from):
        return None

    #se não tiver que pesquisar nas subpastas, simplesmente lista os arquivos no diretorio recebido e verifica a existencia do arquivo desejado
    if not sub_directory:
        if filename in os.listdir(path_from):
            return path.join(path_from, filename)
        return None

    #cria uma lista de resultados (pode haver arquivos com mesmo nome nas subpastas)
    #verifica todos os subdiretorios a procura desse arquivo
    list_out = []
    for dirname, dirnames, filenames in os.walk(path_from):
        for fname in filenames:
            if fname == filename:
                list_out.append(path.join(dirname, fname))

    #se for zero, não encontrou o arquivo, então retorna None
    if len(list_out) == 0:
        return None

    return list_out