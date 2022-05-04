import os

#Essa função serve para trocar o inicio de um diretório por outro
#ex: path1: "aaa/bbb"
#    path2: "fff/ggg"
#path_root: "aaa/bbb/ccc/ddd"

#    saida: "/fff/ggg/ccc/ddd"
def change(path1, path2, path_root, ini=True, end=False):
    p1 = [v for v in path1.split("/") if v != ""]
    p2 = [v for v in path2.split("/") if v != ""]
    pr = [v for v in path_root.split("/") if v != ""]

    if ini:
        pr = pr[len(p1):]
        new_path = []
        new_path.extend(p2)
        new_path.extend(pr)

        new_path = os.path.join(*new_path)
        if not os.path.isabs(new_path) and len(path2) > 0 and path2[0] == '/':
            new_path = "/" + new_path

        return new_path
    else:
        return False

#testes:
if __name__ == "__main__":
    path1 = "/home/wellington/Documentos"
    path2 = ""
    path_root = "/home/wellington/Documentos/itk/bin/teste.png"
    print(path1)
    print(path2)
    print(path_root)
    print(os.path.dirname(change(path1, path2, path_root)))
