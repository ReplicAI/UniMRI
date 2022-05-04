def get():
    DATABASE = {
        "training":[],
        "test":[],
        "filenames":["MRIFreeDataset.zip"]
    }

    #training

    infos = [
        ["AT", "34"], ["AA", "30"], ["GPE", "50"], ["HC", "23"], ["IO", "21"], ["MJ", "23"], ["IPH", "51"], ["KM", "25"],
        ["NP", "30"], ["TA", "18"], ["SE", "19"], ["MME", "28"], ["MK", "29"], ["SST", "43"], ["PM", "45"], ["NGE", "25"],
        ["CP", "54"], ["IY", "40"], ["KKY", "33"], ["PRI", "17"], ["SKS", "20"], ["TZN", "19"], ["ARK", "43"], ["CHP", "30"],
        ["CHE", "46"], ["DK", "28"], ["FA", "18"], ["FI", "28"], ["IG", "23"], ["KAZM", "32"], ["TE", "20"], ["SP", "15"],
        ["KCH", "27"], ["PGE", "28"], ["GSOU", "43"], ["TSA", "28"], ["CK", "30"], ["TZDE", "22"]
    ]

    for i in infos:
        DATABASE["training"].append(
            { 
                "dataset":"ehealth", "MS":True, "sex":"", "age":i[1], "ms_type":"", "filename": "MRIFreeDataset.zip",
                "patient_code": i[0],
                "path_T1":"",
                "path_T2":"",
                "path_FLAIR":"",
                "path_PD":"",
                "path_T1GADO":"",
                "path_lesion":""
            }
        )
    return DATABASE