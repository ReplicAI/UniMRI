import os

#caso tenha uma '/' no final do path, essa função remove
def _fix(path):
    if path[-1] == '/':
        return path[:-1]
    return path

#verifica se o path recebido é um path existente e absoluto, caso não for, retorna False
def verify(path):
    if not os.path.exists(path) or not os.path.isabs(path):
        return False

    return _fix(path)

#junta dois paths
def join(*args):
    return os.path.join(*args)

#retorna o diretório de um arquivo especifico
def dirname(path):
    res = os.path.dirname(path)
    return res

#remove um arquivo
def remove(path):
    return os.remove(path)

#verifica se o path recebido é uma pasta
def isdir(path):
    return os.path.isdir(path)

#verifica se o path recebido é um arquivo
def isfile(path):
    return os.path.isfile(path)

#retorna o ultimo nome de um path, ex: "/home/user/doc.txt" retorna: "/home/user"
def lastname(path):
    sp = path.split("/")
    try:
        return sp[-1] if sp[-1] != "" else sp[-2]
    except:
        return sp[-1]