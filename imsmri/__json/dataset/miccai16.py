def get():
    DATABASE = {
        "training": [],
        "test": [],
        "filenames": ["Unprocessed training dataset"]
    }

    #training
    infos =[
        ["01016SACH", "F", "36"], ["01038PAGU", "M", "41"], ["01039VITE", "F", "26"],
        ["01040VANE", "F", "48"], ["01042GULE", "F", "24"], ["07001MOEL", "M", "53"],
        ["07003SATH", "F", "42"], ["07010NABO", "F", "36"], ["07040DORE", "F", "52"],
        ["07043SEME", "M", "36"], ["08002CHJE", "M", "54"], ["08027SYBR", "F", "55"],
        ["08029IVDI", "M", "35"], ["08031SEVE", "M", "38"], ["08037ROGU", "M", "48"]
    ]

    for v in infos:
        DATABASE["training"].append(
            { 
                "dataset":"miccai16", "MS":True, "sex":v[1], "age":v[2], "ms_type":"", "filename": DATABASE["filenames"][0]+".zip",
                "patient_code": v[0],
                "path_T1":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/3DT1.nii.gz",
                "path_T2":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/T2.nii.gz",
                "path_FLAIR":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/3DFLAIR.nii.gz",
                "path_PD":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/DP.nii.gz",
                "path_T1GADO":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/3DT1GADO.nii.gz",
                "path_lesion":"miccai16/"+DATABASE["filenames"][0].replace(" ", "_")+"/TrainingDataset_MSSEG/"+v[0]+"/Consensus.nii.gz",
            }
        )

    return DATABASE