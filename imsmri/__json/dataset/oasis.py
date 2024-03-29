def get():
    DATABASE = {
        "training":[],
        "test":[],
        "filenames": ["oasis3.zip"],
        "dataset": "oasis"
    }

    infos = [
        ["OAS30759_MR_d0063", "F", "69"], ["OAS30387_MR_d3401", "M", "83"], ["OAS30046_MR_d1968", "M", "85"], ["OAS30479_MR_d2421", "M", "86"], ["OAS30559_MR_d0431", "M", "69"], 
        ["OAS30073_MR_d3670", "M", "71"], ["OAS30817_MR_d1254", "M", "76"], ["OAS30749_MR_d1996", "M", "78"], ["OAS30644_MR_d0136", "F", "69"], ["OAS30671_MR_d2486", "M", "74"], 
        ["OAS30240_MR_d3487", "F", "72"], ["OAS30230_MR_d3855", "F", "56"], ["OAS31149_MR_d0061", "F", "75"], ["OAS30597_MR_d3137", "M", "81"], ["OAS30668_MR_d2432", "F", "54"], 
        ["OAS31165_MR_d1122", "M", "58"], ["OAS31096_MR_d1308", "M", "85"], ["OAS30143_MR_d3509", "F", "68"], ["OAS30328_MR_d0470", "M", "73"], ["OAS30283_MR_d0797", "F", "76"], 
        ["OAS30353_MR_d2635", "F", "64"], ["OAS30372_MR_d4514", "F", "66"], ["OAS30355_MR_d0861", "M", "69"], ["OAS30832_MR_d2369", "F", "67"], ["OAS30361_MR_d3275", "F", "83"], 
        ["OAS30551_MR_d1310", "F", "68"], ["OAS31092_MR_d3113", "M", "80"], ["OAS30315_MR_d0124", "M", "77"], ["OAS30392_MR_d3145", "F", "81"], ["OAS30475_MR_d0062", "F", "72"], 
        ["OAS30127_MR_d0837", "M", "67"], ["OAS30920_MR_d1924", "F", "67"], ["OAS30161_MR_d2517", "F", "64"], ["OAS30184_MR_d3157", "F", "81"], ["OAS30039_MR_d0103", "F", "73"], 
        ["OAS30866_MR_d0640", "F", "79"], ["OAS30970_MR_d0238", "F", "68"], ["OAS30195_MR_d0193", "M", "67"], ["OAS30769_MR_d1547", "M", "72"], ["OAS30062_MR_d1745", "F", "56"], 
        ["OAS30034_MR_d0044", "F", "65"], ["OAS30419_MR_d2360", "F", "53"], ["OAS30002_MR_d2340", "M", "73"], ["OAS30987_MR_d0965", "M", "68"], ["OAS30587_MR_d4511", "F", "76"], 
        ["OAS30438_MR_d2358", "F", "79"], ["OAS30074_MR_d1871", "F", "76"], ["OAS30926_MR_d1520", "M", "82"], ["OAS30960_MR_d2110", "F", "57"], ["OAS31167_MR_d4564", "M", "64"], 
        ["OAS30680_MR_d6255", "M", "89"], ["OAS30589_MR_d3191", "F", "83"], ["OAS30219_MR_d0064", "F", "59"], ["OAS30210_MR_d0047", "F", "83"], ["OAS30845_MR_d1266", "F", "69"], 
        ["OAS30486_MR_d1300", "M", "58"], ["OAS30989_MR_d2594", "F", "58"], ["OAS30819_MR_d0572", "F", "73"], ["OAS30735_MR_d3515", "F", "66"], ["OAS30132_MR_d1392", "M", "71"], 
        ["OAS30818_MR_d2399", "M", "76"], ["OAS30027_MR_d1300", "M", "72"], ["OAS30542_MR_d3116", "M", "80"], ["OAS30729_MR_d6253", "M", "80"], ["OAS30122_MR_d0136", "M", "73"], 
        ["OAS30346_MR_d1685", "F", "76"], ["OAS30857_MR_d2255", "M", "56"], ["OAS30376_MR_d0082", "F", "77"], ["OAS30175_MR_d3219", "F", "81"], ["OAS30647_MR_d1286", "F", "58"], 
        ["OAS30048_MR_d2292", "F", "66"], ["OAS30092_MR_d3727", "F", "68"], ["OAS30013_MR_d0102", "M", "71"], ["OAS30822_MR_d2022", "F", "72"], ["OAS30573_MR_d0515", "F", "70"], 
        ["OAS30951_MR_d3786", "F", "67"], ["OAS31021_MR_d0049", "M", "61"], ["OAS30414_MR_d0030", "M", "73"], ["OAS30403_MR_d3669", "F", "68"]
    ]

    #training

    for i in infos:
        DATABASE["training"].append(
            { 
                "dataset":"oasis", "MS":False, "sex":i[1], "age":i[2], "ms_type":"healthy", "filename": "oasis3.zip",
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
