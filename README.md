# UniMRI Repository

Introduction
-------------------------------------------

This repository contains a python API to preprocess MRI images of healthy and multiple sclerosis patients, based on the NicMs lesion tool.
Adapted to work with JSON, it supports an unlimited number of databases.
The objective of this work is to provide a pre-processed magnetic resonance base for the application of multiple sclerosis lesion classification and segmentation algorithms.

![img_com_rotulos](https://user-images.githubusercontent.com/49326502/90802677-f85a1080-e2ed-11ea-98f2-0cf11adc92d1.png)

-------------------------------------------
Reference
-------------------------------------------


@inproceedings{wvc,
 author = {Wellington Silveira and Rafael Korb and Graçaliz Dimuro and Rodrigo Bem},
 title = {UniMRI: Unified Repository of Magnetic Resonance Images for Multiple Sclerosis Diagnosis},
 booktitle = {Anais do XVII Workshop de Visão Computacional},
 location = {Online},
 year = {2021},
 keywords = {},
 issn = {0000-0000},
 pages = {190--194},
 publisher = {SBC},
 address = {Porto Alegre, RS, Brasil},
 doi = {10.5753/wvc.2021.18912},
 url = {https://sol.sbc.org.br/index.php/wvc/article/view/18912}
}


Contents
-------------------------------------------

1. [Datasets](#datasets)
2. [Instructions for Downloading Data](#download)
3. [Requirements](#req)
4. [Preprocessing Protocol](#protocol)
5. [Instructions for Use](#use)
6. [Adding New Databases](#new)

<a name="datasets"></a>
Datasets
-------------------------------------------

Pre-processing works only with T1, T2 and FLAIR modes, and all three must be present.

![tab](https://user-images.githubusercontent.com/49326502/90802614-e37d7d00-e2ed-11ea-9169-2aeec7ddaff0.png)

NOTE: To maintain the balance between sick and healthy, only 79 exams from the OASIS 3 database are being used.

<a name="download"></a>
Instructions to Download
-------------------------------------------

*ISBI 2015

Link to download [here](https://smart-stats-tools.org/lesion-challenge)

OBS: Make account on site and go to "lesion challenge" - sclerosis - data

-------------------------------------------

*LJUBLJANA

Link to download [here](http://lit.fe.uni-lj.si/tools.php?lang=eng)

OBS: Get all links from "3D MR image database of Multiple Sclerosis patients with white matter lesion segmentations"

-------------------------------------------

*MICCAI08  

Link to download [here](https://www.nitrc.org/frs/?group_id=745)

OBS: Download all urls from "Segmentation Challenge Data"

-------------------------------------------

*MICCAI16

Register on site [here](https://portal.fli-iam.irisa.fr/msseg-challenge/overview?p_p_id=registration_WAR_fliiamportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=3&_registration_WAR_fliiamportlet_mvcPath=%2Fhtml%2Fregistration%2Fregistration.jsp)

OBS: Link to download [here](https://portal.fli-iam.irisa.fr/msseg-challenge/data)

-------------------------------------------

*KIRBY

Link to download [here](https://www.nitrc.org/frs/?group_id=313)

OBS: Select all links from "Kirby 21 (2009)".

-------------------------------------------

*OASIS

Rigister on site [here](https://central.xnat.org/app/template/Register.vm#!)

Link to download [here](https://central.xnat.org/app/template/XDATScreen_report_xnat_projectData.vm/search_element/xnat:projectData/search_field/xnat:projectData.ID/search_value/OASIS3)

OBS: Acess "donwload images" in box "actions.

On "2: select image data" select the boxes NIFTI, FLAIR, T1w and T2w. 

On "3: download data" select "option 2: ZIP download" then submit.

<a name="req"></a>
Requirements
----------------------------------------------------------------

- medpy
- mega.py
- nibabel==2.1.0
- scikit-image
- SimpleITK
- torchvision

<a name="protocol"></a>
Preprocessing protocol
-----------------------------------------------------------------

Protocol:
Images rigid registered on T1 space  
Registered on MNI template  
Anysotropic filter  
Skull-stripping  
Bias field (Intensity inhomogeneity (IIH) or intensity non-uniformity)

---------------------------------------------------------------------------------------------------

<a name="use"></a>
Instructions for using the imsmri package
------------------------------------------------------------------

- [IMSMRI Package](https://github.com/rodrigodebem/iMRI-Dataset/tree/current/imsmri)

<a name="new"></a>
Adding new databases
------------------------------------------------------------------

To add new databases, some internal files can be changed.

For databases that will go through all pre-processing steps:

- 1º: Create file in the "imsmri/__json/dataset" directory with the name of the bank to be added;
- 2ª: Put all exam metadata in the same format as other databases (follow the example of some other file in the same folder);
- 3º: Every directory placed in the dictionary must follow the format:
bank_name/filename_zip/segment_directory_inside_zip;
- 4º: Add the new bank to the file *__init__* in the dataset folder (imsmri/__json/dataset/__init__.py);
- 5º: Add the bank to the __create file (imsmri/__json/__create.py) in the create function;
- 6º: Create variable and its contents with the same name as the database in the file *preprocess* of the imsmri package (imsmri/preprocess.py).

For databases that will only go through data separation (since they are already in the form of a standard image):

- 1º: Create file in the "imsmri/__json/dataset" directory with the name of the bank to be added;
- 2ª: Put all exam metadata in the same format as other databases (follow the example of some other file in the same folder). NOTE: Leave the directories blank;
- 3º: Add the new bank to the file *__init__* in the dataset folder (imsmri/__json/dataset/__init__.py);
- 4º: Add bank to the __create file (imsmri/__json/__create.py) in the create function;
- 5º: Add name of the database (the same informed in the exam metadata) the variable '__exclusions' of the file __create (imsmri/__json/__create.py);
- 6º: Add name of the database (the same informed in the exam metadata) the variable '__exclusions' of the file __change (imsmri/__files/__change.py);
- 7º: Add name of the database (the same informed in the exam metadata) the variable '__exclusions' of the file *__init__* (imsmri/__preprocess/__init__.py);
- 8º: Create file with the name of the database in the folder "imsmri/__preprocess/bank_name" with all the special pre-processing that this bank will have. (follow the example of the "imsmri/__preprocess/ehealth.py" file);
- 9º: Import file created in *__init__* (imsmri/__preprocess/__init__.py);
- 10º: Call the function of the file created in the to_slice function of the file "imsmri/__preprocess/__init__.py" (follow ehealth example);
- 11º: Create variable and its contents with the same name as the database in the file *preprocess* of the imsmri package (imsmri/preprocess.py).

NOTE: When the compressed data file of the new bank has space in the name, put a 'replace(" ", "_")' in the file paths in imsmri/__json/dataset/newbank.py (follow the miccai16 model)
