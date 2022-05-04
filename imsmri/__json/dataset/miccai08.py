def get():
    DATABASE = {
        "training": [],
        "test": [],
        "filenames": [
            "CHB_train_Part1",
            "CHB_train_Part2",
            "CHB_test1_Part1",
            "CHB_test1_Part2",
            "CHB_test1_Part3",
            "UNC_train_Part1",
            "UNC_train_Part2",
            "UNC_test1_Part1",
            "UNC_test1_Part2"
        ]
    }

    part = 1
    for i in range(1, 11):
        if i > 5:
            part = 2

        i_str = str(i)
        if i < 10:
            i_str = "0" + str(i)

        DATABASE["training"].append(
            {
                "dataset":"miccai08", "MS":True, "sex":"", "age":"", "ms_type":"", "filename": "CHB_train_Part"+str(part)+".zip",
                "patient_code": "TRCHB"+i_str,
                "path_T1":"miccai08/"+"CHB_train_Part"+str(part)+"/CHB_train_Case"+i_str+"/CHB_train_Case"+i_str+"_T1.nii.gz",
                "path_T2":"miccai08/"+"CHB_train_Part"+str(part)+"/CHB_train_Case"+i_str+"/CHB_train_Case"+i_str+"_T2.nii.gz",
                "path_FLAIR":"miccai08/"+"CHB_train_Part"+str(part)+"/CHB_train_Case"+i_str+"/CHB_train_Case"+i_str+"_FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":"miccai08/"+"CHB_train_Part"+str(part)+"/CHB_train_Case"+i_str+"/CHB_train_Case"+i_str+"_lesion.nii.gz"
            }
        )
    
    part = 1
    for i in range(1, 11):
        if i > 5:
            part = 2

        i_str = str(i)
        if i < 10:
            i_str = "0" + str(i)

        DATABASE["training"].append(
            {
                "dataset":"miccai08", "MS":True, "sex":"", "age":"", "ms_type":"", "filename": "UNC_train_Part"+str(part)+".zip",
                "patient_code": "TRUNC"+i_str,
                "path_T1":"miccai08/"+"UNC_train_Part"+str(part)+"/UNC_train_Case"+i_str+"/UNC_train_Case"+i_str+"_T1.nii.gz",
                "path_T2":"miccai08/"+"UNC_train_Part"+str(part)+"/UNC_train_Case"+i_str+"/UNC_train_Case"+i_str+"_T2.nii.gz",
                "path_FLAIR":"miccai08/"+"UNC_train_Part"+str(part)+"/UNC_train_Case"+i_str+"/UNC_train_Case"+i_str+"_FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":"miccai08/"+"UNC_train_Part"+str(part)+"/UNC_train_Case"+i_str+"/UNC_train_Case"+i_str+"_lesion.nii.gz"
            }
        )

    #test
    part = 1
    for i in range(1, 18):
        if i > 6:
            part = 2
        if i > 12:
            part = 3

        i_str = str(i)
        if i < 10:
            i_str = "0" + str(i)

        DATABASE["test"].append(
            {
                "dataset":"miccai08", "MS":True, "sex":"", "age":"", "ms_type":"", "filename": "CHB_test1_Part"+str(part)+".zip",
                "patient_code": "TSCHB"+i_str,
                "path_T1":"miccai08/"+"CHB_test1_Part"+str(part)+"/CHB_test1_Case"+i_str+"/CHB_test1_Case"+i_str+"_T1.nii.gz",
                "path_T2":"miccai08/"+"CHB_test1_Part"+str(part)+"/CHB_test1_Case"+i_str+"/CHB_test1_Case"+i_str+"_T2.nii.gz",
                "path_FLAIR":"miccai08/"+"CHB_test1_Part"+str(part)+"/CHB_test1_Case"+i_str+"/CHB_test1_Case"+i_str+"_FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":""
            }
        )
    
    part = 1
    for i in range(1, 15):
        if i == 2:
            continue
        if i > 7:
            part = 2

        i_str = str(i)
        if i < 10:
            i_str = "0" + str(i)

        DATABASE["test"].append(
            {
                "dataset":"miccai08", "MS":True, "sex":"", "age":"", "ms_type":"", "filename": "UNC_test1_Part"+str(part)+".zip",
                "patient_code": "TSUNC"+i_str,
                "path_T1":"miccai08/"+"UNC_test1_Part"+str(part)+"/UNC_test1_Case"+i_str+"/UNC_test1_Case"+i_str+"_T1.nii.gz",
                "path_T2":"miccai08/"+"UNC_test1_Part"+str(part)+"/UNC_test1_Case"+i_str+"/UNC_test1_Case"+i_str+"_T2.nii.gz",
                "path_FLAIR":"miccai08/"+"UNC_test1_Part"+str(part)+"/UNC_test1_Case"+i_str+"/UNC_test1_Case"+i_str+"_FLAIR.nii.gz",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":""
            }
        )

    return DATABASE