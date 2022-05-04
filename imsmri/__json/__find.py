#essa função retorna a localização (no json principal) dos dados de um dataset especifico
#retorna tanto uma lista dos indexadores pra o json principal em forma de list, tanto as keys e indexadores do json principal em forma de dict
def find(dataset, data, all_data):
    itrs = []
    keys = []

    for i in range(len(all_data)):
        if all_data[i]["dataset"] == dataset:
            itrs.append(i)

    for t in range(len(data["training"])):
        if data["training"][t]["dataset"] == dataset:
            keys.append(("training", t))

    for t in range(len(data["test"])):
        if data["test"][t]["dataset"] == dataset:
            keys.append(("test", t))

    return itrs, keys