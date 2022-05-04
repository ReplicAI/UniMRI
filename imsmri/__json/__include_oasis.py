from .. import __path as path
import os

#Como o oasis não segue um padrão em todos os diretórios internos do arquivo compactado
#Essa função caminha por todos os subdiretórios do oasis e cria automaticamente todos os diretórios no json principal
def include_oasis(full_data, ind):
    #ind é todos os indexadores dos dados do oasis no json principal.
    for i in ind:
        patient = full_data[i]["patient_code"]
        filename = full_data[i]["filename"].split(".")[0]
        path_f = path.join(path.files_unzip, full_data[i]["dataset"], filename)

        for dirname, dirnames, filenames in os.walk(path_f):
            #procura a pasta onde estão os dados desse exame, se não for essa pasta, continua
            if path.lastname(dirname) != patient:
                continue

            for dn, dr, fl in os.walk(dirname):
                #aqui, está 'caminhado' dentro da pasta das imagens
                for fname in fl:
                    file = path.join(dn, fname)
                    
                    #se achou T1, T2 ou FLAIR, salva no json seus paths
                    if "T1" in file and full_data[i]["path_T1"] == "":
                        full_data[i]["path_T1"] = file
                        full_data[i]["original_path"] = path.dirname(path.change(path.files_unzip, "", file))
                        full_data[i]["path_T1_pre"] = path.change(path.files_unzip, path.files_pre, file)
                    elif "T2" in file and full_data[i]["path_T2"] == "":
                        full_data[i]["path_T2"] = file
                        full_data[i]["original_path"] = path.dirname(path.change(path.files_unzip, "", file))
                        full_data[i]["path_T2_pre"] = path.change(path.files_unzip, path.files_pre, file)
                    elif "FLAIR" in file and full_data[i]["path_FLAIR"] == "":
                        full_data[i]["path_FLAIR"] = file
                        full_data[i]["original_path"] = path.dirname(path.change(path.files_unzip, "", file))
                        full_data[i]["path_FLAIR_pre"] = path.change(path.files_unzip, path.files_pre, file)
    return True