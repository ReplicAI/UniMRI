import time

#Seleciona os dados a partir do json principal e gera uma lista de todos os dados que se enquadram nos parametros recebidos
#se essa função não receber parametros, ela retorna todos os dados do json principal
def select(database, sex, age, ms, training, test, unknown, all_data):
    new_data = []

    #itera sobre todos os dados
    for data in all_data:
        #se foi especificado algumas databases, verifica se esse exame da iteração
        #pertence a alguma das databases escolhidas, se não, continua pro proximo exame
        if database is not None:
            database = list(map(lambda x: x.upper(), database)) if type(database) != str else database.upper()
            if not data["dataset"].upper() in database and not "all" in database:
                continue

        #se sex não for nulo, quer dizer que o usuario colocou uma função para fazer a verificação da idade
        #é colocado um try/except pois o usuario tem grandes changes de colocar uma função invalida
        if sex is not None:
            try:
                if data["sex"] == "":
                    #muitos dados não tem informações sobre idade e sexo
                    #se o unknown for True, os dados desconhecidos serão considerados
                    #senão, continua
                    if not unknown:
                        continue
                elif not sex(data["sex"]):
                    continue
            except:
                raise Exception("sex: Invalid function!")

        #mesmo caso do sex
        if age is not None:
            try:
                if data["age"] == "":
                    if not unknown:
                        continue
                elif not age(int(data["age"])):
                    continue
            except:
                raise Exception("age: Invalid function!")

        #mesmo caso do sex e age
        if ms is not None:
            try:
                if data["ms_type"] == "":
                    if not unknown:
                        continue
                elif not ms(data["ms_type"]):
                    continue
            except:
                raise Exception("ms: Invalid function!")

        #seleciona se os dados serão de treinamento ou teste
        if not training:
            if data["datatype"] == "training":
                continue

        if not test:
            if data["datatype"] == "test":
                continue
        
        #se passou por todos os estagios e chegou aqui, então esse dado será colocado na lista
        new_data.append(data)

    return new_data