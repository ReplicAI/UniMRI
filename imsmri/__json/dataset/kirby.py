def get():
    DATABASE = {
        "training":[],
        "test":[],
        "filenames": [
            "KKI2009-"+str(v)+".tar.bz2" if v >= 10 else "KKI2009-0"+str(v)+".tar.bz2" for v in range(1, 43)
        ],
        "dataset": "kirby"
    }

    #training
    infos = [
        ['M', '25'], ['F', '61'], ['F', '30'], ['M', '25'], ['M', '25'], ['M', '28'], ['M', '30'],
        ['F', '49'], ['M', '25'], ['F', '38'], ['M', '25'], ['F', '26'], ['M', '30'], ['M', '38'],
        ['M', '34'], ['F', '42'], ['M', '38'], ['M', '26'], ['F', '26'], ['M', '28'], ['F', '38'],
        ['F', '30'], ['F', '29'], ['M', '30'], ['M', '25'], ['M', '34'], ['F', '29'], ['M', '32'],
        ['F', '49'], ['F', '28'], ['M', '25'], ['F', '23'], ['F', '28'], ['M', '30'], ['F', '42'],
        ['F', '23'], ['F', '61'], ['M', '26'], ['F', '22'], ['M', '32'], ['F', '22'], ['M', '26']
    ]

    for i, v in enumerate(infos):
        i_str = str(i+1)
        if i+1 < 10:
            i_str = "0" + str(i+1)

        DATABASE["training"].append(
            { 
                "dataset":"kirby", "MS":False, "sex":v[0], "age":v[1], "ms_type":"healthy", "filename": "KKI2009-"+i_str+".tar.bz2",
                "patient_code": i_str,
                "path_T1":"kirby/"+"KKI2009-"+i_str+"/KKI2009-"+i_str+"-MPRAGE.nii.gz",
                "path_T2":"kirby/"+"KKI2009-"+i_str+"/KKI2009-"+i_str+"-T2w.nii.gz",
                "path_FLAIR":"kirby/"+"KKI2009-"+i_str+"/KKI2009-"+i_str+"-FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":""
            }
        )

    return DATABASE