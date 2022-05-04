from .. import __path as path
from .. import __json as json
from . import __read as read
import shutil

#importa o pytorch
import torchvision
from torchvision import transforms

#caso seja convertido em tensor e o transform seja True, será usada essa tranformação padrao
#deixando a imagem 224x224
__default_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor()
    #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

#Essa função é usada depois dos dados serem pré processados. Ela abre o json das imagens geradas pelo to_slice
#e preenche as listas (definidas no __init__) com as imagens e seus metadados
def load(Path):
    #se o path for None, o path padrão é usado
    if Path is None:
        Path = path.files_out
    
    #se o json não for encontrado na pasta das imagens, uma exceção será gerada
    #o arquivo json SEMPRE deve estar junto das imagens, nunca deve ser removido, pois ele indexa todas as imagens e seus metadados
    if not path.isfile(path.join(Path, "final_json.json")):
        raise Exception("Images load: '"+str(path.join(Path, "final_json.json"))+"' file not found!")

    #abre o json instanciando a classe final_json que contem funções pra manipulação do mesmo
    myjson = json.__final_json__.final_json()
    myjson.load(Path)
    #carrega todos os dados presenter no json
    data = myjson.data()

    x_training = []
    y_training = []

    x_validation = []
    y_validation = []
    
    x_test = []
    y_test = []

    #esse for é usado para os dados de treinamento e teste presente no json
    #lembrando que o json contem um dicionario com dois indexadores ('training', 'test')
    for tipo in ["training", "test"]:
        #itera sobre todos os metadados de dentro do json
        for file in data[tipo]:
            #caso o arquivo não exista no disco (deveria existir, se não existe, algo que não deveria aconteceu e seria necessario revisar todos os dados)
            if not path.isfile(path.join(Path, data[tipo][file]["local_path"])):
                raise Exception("Images load: '"+str(path.join(Path, data[tipo][file]["local_path"]))+"' file not found!")

            #used_as é um indexador que é recebido quando os dados são separados
            #se não existir, os dados não foram separados em treinamento, validação e teste
            if not "used_as" in data[tipo][file].keys():
                raise Exception("Data has not been separated.")

            #se o dado for usado como treinamento, validação ou teste
            #lê a imagem do disco e seu rotulo, colocando-os nas listas de dados
            if data[tipo][file]["used_as"] == "training":
                x_training.append(read.image(path.join(Path, data[tipo][file]["local_path"])))
                y_training.append(data[tipo][file])
            elif data[tipo][file]["used_as"] == "validation":
                x_validation.append(read.image(path.join(Path, data[tipo][file]["local_path"])))
                y_validation.append(data[tipo][file])
            else:
                x_test.append(read.image(path.join(Path, data[tipo][file]["local_path"])))
                y_test.append(data[tipo][file])

    #salva qualquer alteração que o json sofreu
    myjson.save()
    #retorna todos os dados carregados
    return x_training, y_training, x_validation, y_validation, x_test, y_test

#lê os dados da mesma maneira que o outro load, porém transforma em tensores e os retorna
def load_tensor(Path=None, to_tensor=False, transform=None):
    global __default_transform
    if Path is None:
        Path = path.files_out

    #explicado no primeiro load
    if not path.isfile(path.join(Path, "final_json.json")):
        raise Exception("Images load: '"+str(path.join(Path, "final_json.json"))+"' file not found!")

    myjson = json.__final_json__.final_json()
    myjson.load(Path)
    data = myjson.data()

    for tipo in ["training", "test"]:
        for file in data[tipo]:
            if not path.isfile(path.join(Path, data[tipo][file]["local_path"])):
                continue

            if not "used_as" in data[tipo][file].keys():
                raise Exception("Data has not been separated.")

            #para que o pytorch carregue os dados e seus rotulos, os dados tem que ser movidos
            #para as pastas correspondentes a seus rotulos, aqui, a pasta que contém 1 (bool) será um exame doente
            #e a pasta com o nome de 0 (bool) para exames saudaveis
            for folder in ["training", "validation", "test"]:
                #se as pastas training, validation e test não existirem, os dados não foram separados
                #pois essas pastas são criadas na função separate
                if not path.isdir(path.join(Path, folder)):
                    raise Exception("Data has not been separated.")
                
                #cria as pastas 0 e 1
                if not path.isdir(path.join(Path, folder, "0")):
                    path.mkdirs(path.join(Path, folder, "0"))
                if not path.isdir(path.join(Path, folder, "1")):
                    path.mkdirs(path.join(Path, folder, "1"))

            for mode in ["training", "validation", "test"]:
                if data[tipo][file]["used_as"] == mode:
                    #se for doente, a variavel fl recebe '1', senão recebe '0'
                    fl = "1" if bool(data[tipo][file]["MS"]) else "0"

                    #se a imagem não existir, algo de errado aconteceu e alguma imagem foi apagada
                    if not path.isfile(path.join(Path, data[tipo][file]["local_path"])):
                        raise Exception("Images load: '"+str(path.join(Path, data[tipo][file]["local_path"]))+"' file not found!")

                    #as imagens devem ser movidas para as pastas criadas (0 e 1)
                    shutil.move(
                        path.join(Path, data[tipo][file]["local_path"]),
                        path.join(Path, mode, fl)
                    )
                    #atualiza o json informando qual o novo diretorio da imagem:
                    sep = data[tipo][file]["local_path"].split("/")
                    #salva o nome da imagem e last e coloca o nome da nova pasta na ultima posição da lista
                    last, sep[-1] = sep[-1], fl
                    #depois coloca o nome do arquivo novamente e junta tudo
                    sep.append(last)
                    data[tipo][file]["local_path"] = path.join(*sep)

    #se transform for None, a transformação padrão será usada para normalizar os dados
    if transform is None:
        transform = __default_transform

    #cria os conjuntos de dados usando a própria biblioteca do pytorch
    train_set = torchvision.datasets.ImageFolder(root=path.join(Path, "training"), transform=transform)
    val_set = torchvision.datasets.ImageFolder(root=path.join(Path, "validation"), transform=transform)
    test_set = torchvision.datasets.ImageFolder(root=path.join(Path, "test"), transform=transform)

    #salva o json com as alterações que teve
    myjson.save()
    #retorna o path, e os três conjuntos de dados
    return Path, train_set, val_set, test_set

#testes:
if __name__ == "__main__":
    if type(__default_transform) == transforms.Compose:
        print("ok")