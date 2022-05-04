from .. import __path as path
import json

#Essa classe é usada para criar e manipular o json que fica junto com as imagens geradas pelo pré processamento to_slice
#Esse é o json responsável por gerenciar todas as imagens finais e fica dentro da pasta Pre/images_out
class final_json:
    #nome do arquivo
    filename = "final_json.json"

    def __init__(self):
        self._data = None
        #como essa classe é usada pelo pré-processamento to_slice, o path padrão é usado
        #a variavel self.mode serve para definir que a classe ta sendo usada em outro diretorio não padrão
        #toda função faz o load automatico do json, mas quando a variavel self.mode é True, o load não carrega novamente, o que é o certo
        self.mode = False
        #path onde se encontra o arquivo json
        self.path_folder = ""

    def _load(self, path_file=None):
        #recebe o path do json e coloca na variavel, se não receber, o path padrão é usado
        path_json = path.files_out if path_file is None else path_file
        #se self.__data não é nulo, quer dizer que algum json já foi carregado
        #e se o self.mode for True, os dados já foram carregados de algum diretório
        if self._data is not None and path_file is None or self.mode:
            return False

        if path_file is not None:
            #define que o load foi feito em um path diferente do padrão
            self.mode = True

        #Lê o conteudo do json, caso ele não exista, é criado
        if path.isfile(path.join(path_json, self.__class__.filename)):
            #atualiza o path do json
            self.path_folder = path_json
            #lê o arquivo
            with open(path.join(path_json, self.__class__.filename), "r") as f:
                self._data = json.load(f)

            return True

        #caso o arquivo não exista, o path será atualizado com o path recebido ou o padrão
        self.path_folder = path_json
        self.mode = False
        #cria a lista de dados vazia para ser preenchida pelos dados separados pelo to_slice
        self._data = {
            "training": {},
            "test": {}
        }
        return False

    #le o arquivo de um local diferente
    def load(self, path_json, force=False):
        #force serve para recarregar algum outro arquivo
        if force:
            self.mode = False
        return self._load(path_file=path_json)

    #salva o json
    def save(self):
        #se tiver algum problema com o path que foi definido, uma exceção é gerada
        if not path.isdir(self.path_folder) or self.path_folder == "":
            raise Exception("final_json: '"+self.path_folder+"' invalid directory")

        #salva o json
        with open(path.join(self.path_folder, self.__class__.filename), "w") as f:
            json.dump(self._data, f)

    #verifica a existencia de algum paciente no json, precisa especificar o banco de dados e o codigo do paciente (definido na criação dos dbs)
    def ispatient(self, dataset, patient_code):
        self._load()
        for mod in self._data:
            for key in self._data[mod]:
                #key contém a chave que é o mesmo nome da imagem, e o nome da imagem contém o nome do banco e o codigo
                #nesse formato: NOMEBANCO_CODIGOPACIENTE_CONTAGEMIMAGEM.format
                info = key.split("_")
                #retira o formato e a contagem:
                info = info[:-1]
                #junta o codigo novamente (as vezes o codigo é, também, separado por '_' (oasis))
                code = '_'.join(info[1:]) if len(info[1:]) > 1 else info[1]
                #se existir, retorna True
                if info[0] == dataset.upper() and code == patient_code:
                    return True
        return False

    #recebe o nome (na verdade a key) e retorna todas as informações desse exame
    def get_patient(self, name):
        self._load()
        for mod in self._data:
            for key in self._data[mod]:
                if key == name:
                    return self._data[mod][key]
        return False

    #embora não usado, retorna todos os metadados de todas as imagens
    def get_all_patient(self):
        list_all = []
        for mod in self._data:
            for key in self._data[mod]:
                list_all.append(key)

        return list_all

    #remove uma imagem do json (mas não apaga a imagem do disco)
    def remove_patient_and_key(self, keyname):
        self._load()
        for mod in self._data:
            for key in self._data[mod]:
                if key == keyname:
                    #print("del:",key)
                    if path.isfile(path.join(self.path_folder, self._data[mod][key]["local_path"])):
                        path.remove(path.join(self.path_folder, self._data[mod][key]["local_path"]))
                        #print("remove file:", self._data[mod][key]["local_path"])

                    self._data[mod].pop(key)
                    self.save()
                    return True
        return False

    #Insere uma nova imagem ao json
    def insert(self, data):
        self._load()
        self._data[data["datatype"]][path.lastname(data["local_path"])] = data
        self.save()

    #deleta todas as imagens de um determinado exame e apaga as imagens do disco
    def delete_exam(self, dataset, patient_code, del_files=True):
        self._load()
        del_itens = []
        for mod in self._data:
            for key in self._data[mod]:
                #mesmo sistema do ispatient
                info = key.split("_")
                info = info[:-1]
                code = '_'.join(info[1:]) if len(info[1:]) > 1 else info[1]
                if info[0] == dataset.upper() and code == patient_code:
                    #se o paciente existir, coloca na lista para ser apagado
                    #salva os indexadores (mod, key) e o local relativo da imagem no disco
                    del_itens.append([mod, key, self._data[mod][key]["local_path"]])

        #percorre a lista dos dados a serem apagados
        for v in del_itens:
            #apaga a imagem do json
            self._data[v[0]].pop(v[1])

            if del_files:
                #se a imagem existir, deleta ela do disco
                if self.path_folder != "" and path.isfile(path.join(self.path_folder, v[2])):
                    path.remove(path.join(self.path_folder, v[2]))

        #salva o json
        self.save()
        #informa quantos dados foram apagados
        return len(del_itens)

    #Retorna o conteudo atual do json
    def data(self):
        self._load()
        return self._data

'''

{
    "training": {
        "chave (name file1)": {"atributos"},
        "chave (name file2)": {"atributos"},
        "chave (name file3)": {"atributos"}
    },
    "test": {
        "chave (name file1)": {"atributos"}
    },
}

'''