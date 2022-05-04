import nibabel as nib
import numpy as np
from datetime import datetime

from .. import __path as path
from .. import __files as files
from .. import __json as json
from .. import __images as images

__porcent_ini = 20
__porcent_end = 20

#small é o maior porque somente vai salvar as imagens com uma soma (da lesão) maior que 1% da imagem original
#large é o menor porque vai salvar as imagens com uma soma (da lesão) maior que 0.05% (quase todas) da imagem original
__porcent_small = 1
__porcent_medium = 0.35
__porcent_large = 0.05

#salva as etapas desse pré processamento num arquivo de log
def save_log(msg):
    tn = datetime.now()
    timenow = tn.strftime("[%d/%m/%Y %H:%M:%S] ")
    msg_completa = timenow + msg + "\n"

    frases = []
    try:
        with open(path.log_file, "r") as f:
            frases = f.readlines()
    except:
        pass
    finally:
        frases.append(msg_completa)
        with open(path.log_file, "w") as f:
            f.writelines(frases)
'''
def save_f(name, matriz):
    with open(path.join(path.resource, name+".txt"), "w") as f:
        f.write(str([matriz[v, :] for v in range(matriz.shape[0])]))
'''

#essa função serve para retornar o inicio e fim em que contenha mais informações sobre o cerebro
#desconsiderando o inicio e o fim. Se a soma da matriz for maior que um limite, ele retorna o ini e o fim
def lim(matriz, view, center, db):
    global __porcent_ini, __porcent_end
    tam = matriz.shape

    save_log("view: "+view)
    if view == "sagittal":
        if not center:
            return 0, tam[0]

        ini = 0
        end = tam[0]

        for i in range(tam[0]):
            aux = np.copy(matriz[i,:,:])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_ini:
                ini = i
                save_log("index ini: "+str(ini)+", sum: "+str(np.sum(aux)))
                break

        for i in range(tam[0]-1, -1, -1):
            aux = np.copy(matriz[i,:,:])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_end:
                end = i
                save_log("index end: "+str(end)+", sum: "+str(np.sum(aux)))
                break

        ini = ini if ini >= int(0.15*tam[0]) else int(0.2*tam[0])
        end = end if end <= (tam[0] - int(0.15*tam[0])) else (tam[0] - int(0.2*tam[0]))

        return ini, end

    elif view == "front":
        if not center:
            return 0, tam[1]

        ini = 0
        end = tam[1]

        for i in range(tam[1]):
            aux = np.copy(matriz[:,i,:])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_ini:
                ini = i
                save_log("index ini: "+str(ini)+", sum: "+str(np.sum(aux)))
                break

        for i in range(tam[1]-1, -1, -1):
            aux = np.copy(matriz[:,i,:])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_end:
                end = i
                save_log("index end: "+str(end)+", sum: "+str(np.sum(aux)))
                break

        ini = ini if ini >= int(0.15*tam[1]) else int(0.2*tam[1])
        end = end if end <= (tam[1] - int(0.15*tam[1])) else (tam[1] - int(0.2*tam[1]))

        return ini, end

    elif view == "axial":
        if not center:
            return 0, tam[2]

        ini = 0
        end = tam[2]

        for i in range(tam[2]):
            aux = np.copy(matriz[:,:,i])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_ini:
                ini = i
                save_log("index ini: "+str(ini)+", sum: "+str(np.sum(aux)))
                break

        for i in range(tam[2]-1, -1, -1):
            aux = np.copy(matriz[:,:,i])
            aux[aux > 0.1] = 1
            if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > __porcent_end:
                end = i
                save_log("index end: "+str(end)+", sum: "+str(np.sum(aux)))
                break

        ini = ini if ini >= int(0.15*tam[2]) else int(0.2*tam[2])
        end = end if end <= (tam[2] - int(0.15*tam[2])) else (tam[2] - int(0.2*tam[2]))

        return ini, end

#obtem o nome do arquivo no formado 'NOMEBANCO_PATIENT_NUM.FORMATO', caso já exista, ele incrementa o NUM até que não tenha outro igual
def get_name(data, form, num=0):
    path_out = path.join(path.files_out, data["dataset"].upper()+"_"+data["patient_code"]+"_"+str(num)+"."+form)
    if not path.isdir(path.files_out):
        path.mkdirs(path_out)

    if files.find(path.dirname(path_out), path.lastname(path_out)) is not None:
        return get_name(data, form, num=num+1)
    return path_out

#weighting = T1, T2, FLAIR.
#sensitivity = s, m, l. (small, medium, large) 2000, 500, 15
def process(data, view="axial", max_imgs=10, weighting="T2", center=True, dim=None, form="jpg", synchronize=False, sensitivity= "l"):
    global __porcent_small, __porcent_medium, __porcent_large
    lesion = None
    matriz = None

    save_log("file: dataset: {0}, sex: {1}, age: {2}, ms: {3}, filezip: {4}".format(
            data["dataset"],
            data["sex"],
            data["age"],
            data["MS"],
            data["filename"]
        ))

    try:
        if path.isfile(data["path_T2_pre"]):
            if not path.isdir(path.join(path.resource, "debug")):
                path.mkdirs(path.join(path.resource, "debug"))

            matriz = nib.load(data["path_T2_pre"])
            if not path.isfile(path.join(path.resource, "debug", data["dataset"].upper()+"_"+data["patient_code"]+".jpg")):
                images.save(
                    path.join(path.resource, "debug", data["dataset"].upper()+"_"+data["patient_code"]+".jpg"),
                    matriz.get_data()[:,:,90]
                )
    except Exception as e:
        save_log(e)

    #verificar se esse paciente já foi preprocessado
    if json.__final_json.ispatient(data["dataset"], data["patient_code"]):
        save_log("Existing exam: deleting...")
        json.__final_json.delete_exam(data["dataset"], data["patient_code"])

    #comparar com a lesion mask para pegar as imagens que mais mostram o problema
    if synchronize and data["path_lesion"] != "" and data["datatype"] == "training":
        if path.isfile(data["path_lesion_pre"]):
            lesion = nib.load(data["path_lesion_pre"])
        else:
            lesion = nib.load(data["path_lesion"])

        lesion = lesion.get_data()
        save_log("lesion: "+str(lesion.shape))

    #abre a imagem com o ponderamento escolhido
    for mod in ["path_T1", "path_T2", "path_FLAIR"]:
        if weighting in mod:
            save_log("weighting:"+weighting)
            if path.isfile(data[mod+"_pre"]):
                matriz = nib.load(data[mod+"_pre"])
            else:
                matriz = nib.load(data[mod])

            matriz = matriz.get_data()
            save_log("matriz: "+str(matriz.shape))
            break

    all_imgs = []
    ini, end = lim(matriz, view, center, data["dataset"])
    save_log("final ini: "+str(ini)+", final end: "+str(end))
    limit = {"l": __porcent_large, "m": __porcent_medium, "s": __porcent_small}
    limit = limit[sensitivity]
    save_log("limit: "+str(limit))

    #se for none, coloca todas as imagens em um vetor
    if lesion is None:
        save_log("lesion is None")
        if view == "sagittal":
            for i in range(ini, end):
                all_imgs.append(matriz[i,:,:])
        elif view == "front":
            for i in range(ini, end):
                all_imgs.append(matriz[:,i,:])
        else:
            for i in range(ini, end):
                all_imgs.append(matriz[:,:,i])
    #se não, coloca somente as imagens em que a soma da mascara de lesão for maior que um limite
    else:
        if view == "sagittal":
            for i in range(ini, end):
                aux = np.copy(lesion[i,:,:])
                aux[aux > 0.1] = 1
                if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > limit:
                    save_log("saving. view: "+view+", sum lesion: "+str(np.sum(aux))+", limit: "+str(limit))
                    all_imgs.append(matriz[i,:,:])
        elif view == "front":
            for i in range(ini, end):
                aux = np.copy(lesion[:,i,:])
                aux[aux > 0.1] = 1
                if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > limit:
                    save_log("saving. view: "+view+", sum lesion: "+str(np.sum(aux))+", limit: "+str(limit))
                    all_imgs.append(matriz[:,i,:])
        else:
            for i in range(ini, end):
                aux = np.copy(lesion[:,:,i])
                aux[aux > 0.1] = 1
                if (np.sum(aux) / float(aux.shape[0]*aux.shape[1])) * 100 > limit:
                    save_log("saving. view: "+view+", sum lesion: "+str(np.sum(aux))+", limit: "+str(limit))
                    all_imgs.append(matriz[:,:,i])

    #configura o passo para 'andar' pelo vetor e ir salvando as imagem em formato padrao
    step = int(len(all_imgs) / max_imgs)
    step = 1 if step == 0 else step

    save_log("used step: "+str(step))
    save_log("tam all_imgs: "+str(len(all_imgs)))

    cont, itr = 0, 0
    while cont < max_imgs:
        if itr >= len(all_imgs):
            break

        name = get_name(data, form, num=itr)

        #salva as imagens
        js = json.__file_data(data)
        js["view"] = view
        js["weighting"] = weighting
        js["local_path"] = path.lastname(name)

        images.save(name, all_imgs[itr], tam=dim)
        json.__final_json.insert(js)

        itr += step
        cont += 1
    
    save_log("Done.")
    save_log("------------------------------------------")