def get():
    DATABASE = {
        "training": [],
        "test": [],
        "filenames": ["training_final_v4", "testdata_website_2016-03-24"]
    }

    #training
    for i in range(1, 6):
        ms_type = "RR"
        if i == 4:
            ms_type = "CIS"
        elif i == 5:
            ms_type = "PP"

        DATABASE["training"].append(
            { 
                "dataset":"isbi", "MS":True, "sex":"", "age":"", "ms_type": ms_type, "filename": DATABASE["filenames"][0]+".zip",
                "patient_code": "TR"+str(i),
                "path_T1":"isbi/"+DATABASE["filenames"][0]+"/training/training0"+str(i)+"/orig/training0"+str(i)+"_01_mprage.nii.gz",
                "path_T2":"isbi/"+DATABASE["filenames"][0]+"/training/training0"+str(i)+"/orig/training0"+str(i)+"_01_t2.nii.gz",
                "path_FLAIR":"isbi/"+DATABASE["filenames"][0]+"/training/training0"+str(i)+"/orig/training0"+str(i)+"_01_flair.nii.gz",
                "path_PD":"isbi/"+DATABASE["filenames"][0]+"/training/training0"+str(i)+"/orig/training0"+str(i)+"_01_pd.nii.gz",
                "path_T1GADO":"",
                "path_lesion":"isbi/"+DATABASE["filenames"][0]+"/training/training0"+str(i)+"/masks/training0"+str(i)+"_01_mask1.nii.gz"
            }
        )

    #test
    for i in range(1, 15):
        i_str = str(i)
        if i < 10:
            i_str = "0" + str(i)
        DATABASE["test"].append(
            { 
                "dataset":"isbi", "MS":True, "sex":"", "age":"", "ms_type": "", "filename": DATABASE["filenames"][1]+".zip",
                "patient_code": "TS"+str(i),
                "path_T1":"isbi/"+DATABASE["filenames"][1]+"/testdata_website/test"+i_str+"/orig/test"+i_str+"_01_mprage.nii.gz",
                "path_T2":"isbi/"+DATABASE["filenames"][1]+"/testdata_website/test"+i_str+"/orig/test"+i_str+"_01_t2.nii.gz",
                "path_FLAIR":"isbi/"+DATABASE["filenames"][1]+"/testdata_website/test"+i_str+"/orig/test"+i_str+"_01_flair.nii.gz",
                "path_PD":"isbi/"+DATABASE["filenames"][1]+"/testdata_website/test"+i_str+"/orig/test"+i_str+"_01_pd.nii.gz",
                "path_T1GADO":"",
                "path_lesion":""
            }
        )

    return DATABASE