import sys, os

#Essa função recebe dois paths e retorna a diferença (se o incio de ambos for o mesmo)
#Ex: path_b: "/aaa/bbb/ccc/ddd"
#    path_s: "/aaa/bbb"

#     saida: "ccc/ddd"
def diference(path_b, path_s):
    n_path_b = [v for v in path_b.split("/") if v != ""]
    n_path_s = [v for v in path_s.split("/") if v != ""]

    dif = n_path_b[len(n_path_s):]

    return os.path.join("", *dif)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit(1)

    print(diference(sys.argv[1], sys.argv[2]))