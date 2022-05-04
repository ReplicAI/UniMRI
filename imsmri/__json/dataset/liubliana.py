def get():
    DATABASE = {
        "training":[],
        "test":[],
        "filenames": [
            "patient01-05",
            "patient06-10",
            "patient11-15",
            "patient16-20",
            "patient21-25",
            "patient26-30"
        ]
    }

    #training
    infos = [
        ['patient01-05', 'F', '31', 'RR'], ['patient01-05', 'M', '33', 'CIS'], ['patient01-05', 'F', '37', ''],
        ['patient01-05', 'M', '25', 'SP'], ['patient01-05', 'F', '33', 'RR'], ['patient06-10', 'F', '37', 'SP'],
        ['patient06-10', 'F', '53', 'RR'], ['patient06-10', 'M', '41', 'RR'], ['patient06-10', 'F', '40', 'RR'],
        ['patient06-10', 'F', '64', 'RR'], ['patient11-15', 'M', '29', 'RR'], ['patient11-15', 'F', '39', 'RR'],
        ['patient11-15', 'M', '26', 'RR'], ['patient11-15', 'M', '42', 'RR'], ['patient11-15', 'F', '57', 'PR'],
        ['patient16-20', 'F', '42', 'RR'], ['patient16-20', 'F', '27', 'RR'], ['patient16-20', 'F', '60', 'RR'],
        ['patient16-20', 'F', '47', 'RR'], ['patient16-20', 'F', '37', 'RR'], ['patient21-25', 'F', '33', 'RR'],
        ['patient21-25', 'F', '30', 'RR'], ['patient21-25', 'F', '39', 'RR'], ['patient21-25', 'M', '43', 'RR'],
        ['patient21-25', 'F', '35', 'RR'], ['patient26-30', 'F', '40', 'RR'], ['patient26-30', 'F', '39', 'RR'],
        ['patient26-30', 'F', '39', 'RR'], ['patient26-30', 'F', '26', 'CIS'], ['patient26-30', 'F', '54', 'RR']
    ]

    for i, v in enumerate(infos):
        i_str = str(i+1)
        if i+1 < 10:
            i_str = "0" + str(i+1)

        DATABASE["training"].append(
            {
                "dataset":"liubliana", "MS":True, "sex":v[1], "age":v[2], "ms_type":v[3], "filename": v[0]+".zip",
                "patient_code": i_str,
                "path_T1":"liubliana/"+v[0]+"/patient"+i_str+"/raw/patient"+i_str+"_T1W.nii.gz",
                "path_T2":"liubliana/"+v[0]+"/patient"+i_str+"/raw/patient"+i_str+"_T2W.nii.gz",
                "path_FLAIR":"liubliana/"+v[0]+"/patient"+i_str+"/raw/patient"+i_str+"_FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":"liubliana/"+v[0]+"/patient"+i_str+"/patient"+i_str+"_consensus_gt.nii.gz"
            }
        )

    return DATABASE