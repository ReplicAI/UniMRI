__all__ = []

from . import __include_oasis, __find
from . import __create as __create_json
from . import __select as __select__
from . import __final_json as __final_json__
import json as js

#Variaveis que receberão o json principal
__data = {}
__full_data = []
#variavel com os dados selecionados a partir do json principal
__select_data = []

#funções do pacote json padrão
__dump = js.dump
__load = js.load
__loads = js.loads

#instancia principal da classe final_json
__final_json = __final_json__.final_json()

#retorna os dados em forma de dicionario
def data():
    global __data
    return __data

#retorna os dados em forma de lista
def datalist():
    global __full_data
    return __full_data

#retorna os dados selecionados em forma de lista
def selected_data():
    global __select_data
    return __select_data

#cria o json principal
def __create():
    global __data, __full_data
    __data = __create_json.create()
    __full_data = []
    __full_data.extend(__data["training"])
    __full_data.extend(__data["test"])
    return True

#seleciona os dados que serão usados para fazer o pré-processamento
def __select(database=None, sex=None, age=None, ms=None, training=True, test=True, unknown=False):
    global __full_data, __select_data
    if not __full_data:
        raise Exception("Uninitialized databases!")

    __select_data = __select__.select(database, sex, age, ms, training, test, unknown, __full_data)
    return __select_data

#cria uma interface pra função include_oasis
def __include__oasis():
    global __data, __full_data
    return __include_oasis.include_oasis(__full_data, __find.find("oasis", __data, __full_data)[0])

#essa função recebe o metadado completo de um exame e retorna somente as informações relevantes para o exame em si
#deixando de lado todos os paths e codigos de paciente
def __file_data(data):
    return {
        "dataset": data["dataset"],
        "MS": data["MS"],
        "sex": data["sex"],
        "age": data["age"],
        "ms_type": data["ms_type"],
        "filename": data["filename"],
        "datatype": data["datatype"]
    }