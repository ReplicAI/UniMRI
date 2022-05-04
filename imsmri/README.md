# IMSMRI Package

This package is divided into two main modules, the 'preprocess' and the 'dataloader'. It also contains a communication sub-package with the Mega API for downloading/uploading data, an image manipulation sub-package and a sub-package containing the pre-processing functions.

## Sub Packages

- [API](https://github.com/rodrigodebem/iMRI-Dataset/tree/current/imsmri/api)
- [image](https://github.com/rodrigodebem/iMRI-Dataset/tree/current/imsmri/__images)
- [preprocess](https://github.com/rodrigodebem/iMRI-Dataset/tree/current/imsmri/__preprocess)

NOTE: To access the 'image' and 'preprocess' sub-packages, it will be necessary to access through two variables in the main modules:

*preprocess*: functions (variable that points to the preprocess sub-package)

*dataloader*: image (variable that points to the image sub-package)

## Contents

1. [preprocess](#pre)
2. [dataloader](#datald)
3. [Exemples](#exe)
4. [Google Colab](#colab)

<a name="pre"></a>

## PREPROCESS

The 'preprocess' module has the function of preprocessing magnetic resonance images.

**Constants:**

*Datasets*

- *isbi*
- *miccai08*
- *miccai16*
- *liubliana*
- *kirby*
- *oasis*
- *ehealth*
- *all_databases*

*General*

- *male*
- *female*
- *healthy*

*Constants for pre-processing adjustment*

- *view.front*
- *view.sagittal*
- *view.axial*

- *weighting.T1*
- *weighting.T2*
- *weighting.FLAIR*

- *sensitivity.small*
- *sensitivity.medium*
- *sensitivity.large*

*Constant for the preprocess subpackage*

- *functions*

### Functions

1. [load](#f_load)
2. [select](#f_select)
3. [sequence](#f_sequence)
4. [run](#f_run)
5. [define](#f_def)

<a name="f_load"></a>

### - load(*path_datasets*, *path_pre*)

Initializes internal variables. Its use is mandatory before pre-processing.

**PARAMETERS**

- **path_datasets**: Directory of the original databases.

NOTE: This is the directory where the data will be downloaded (if you use the Mega API)

- **path_pre**: Destination directory of pre-processed data.

**RETURN**

Returns a json containing all data for all exams present in that package.

<a name="f_select"></a>

### - select(*database=None*, *sex=None*, *age=None*, *ms=None*, *training=True*, *test=True*, *unknown=False*)

Selects the data to be pre-processed. All parameters are optional. If all parameters are omitted, all data will be selected.

**PARAMETERS**

- **database=None**: Select one or more databases to use.

- **sex=None**: This parameter receives a function to make the sex selection.

NOTE: The function must receive a single parameter and return a boolean value (EX: lambda x: x == preprocess.male)

- **age=None**: This parameter receives a function to make the age selection.

NOTE: The function must receive a single parameter and return a boolean value (EX: lambda x: x > 30)

- **ms=None**: This parameter receives a function to make the selection according to the exam status (sick or healthy).

NOTE: The function must receive a single parameter and return a boolean value (EX: lambda x: x != preprocess.healthy)

- **training=True**: This parameter receives True to select training data (default: True)

- **test=True**: This parameter receives True to select test data (default: True)

- **unknown=False**: This parameter receives True for selecting data that does not have complete metadata (default: False)

**RETURN**

Returns a json containing the selected data.

<a name="f_sequence"></a>

### - sequence(**args*, *download=True*, *upload=True*)

Select which preprocessing functions will be used. Only pre-processing functions are accepted (sub-package imsmri.__preprocess).

**PARAMETERS**

- ***args**: This parameter receives a list of pre-processing functions.

- **download=True**: Selects whether the data will be downloaded or not (if the data is present in the Mega).

- **upload=True**: If set to True, preprocessed data (3D scans) will be sent to Mega.

**RETURN**

None

<a name="f_run"></a>

### - run(*to=-1*, *init=False*, *replace=False*, *continue_from_mega=False*)

This function starts the pre-processing of the data using the selected data and the functions indicated in the 'sequence' function.

**PARAMETERS**

- **to=-1**: Defines the amount of data that will be pre-processed.

- **init=False**: Defines whether to start preprocessing from the beginning (When data is preprocessed, a temporary file is created indicating which data has already been preprocessed. If the program is closed, it will return to where it left off, but only if init is False).

- **replace=False**: When this parameter is True, if the selected exam has already been preprocessed, the function deletes the preprocessed files and preprocesses again. If it is False, the function moves to the next exam.

- **continue_from_mega=False**: When this parameter is True, the function will download the 'images_out' folder containing pre-processed images (if any) from Mega. With that, the preprocessing continues where it left off.

**RETURN**

None

<a name="f_def"></a>

### - define(*max_imgs=10*, *dim=()*, *center=True*, *synchronize=False*, *format_out="jpg"*, *view="axial"*, *weighting="T2"*, *sensitivity="l"*)

**PARAMETERS**

- **max_imgs=10**: This parameter defines the maximum number of images that will be generated from an exam.

- **dim=()**: This parameter defines the output dimensions of the images (ex: dim = (224,224)).

- **center=True**: This parameter defines whether the external parts of the exam (where it does not contain the brain) will be considered (If True, it will ignore the external parts).

- **synchronize=False**: When exams have a lesion mask, there is the possibility to generate images only where the lesion mask is segmented, thus ensuring that the exit images contain the problem and not a healthy image (even in a sick brain, there is the possibility of some slice will be healthy).

If the 'synchronize' parameter is True, the imager will synchronize the lesion mask with the exam to generate the output images.

- **format_out="jpg"**: This parameter defines the output format of the images.

- **view="axial"**: This parameter defines which view will be considered when generating the images (see the constants section).

- **weighting="T2"**: This parameter defines what weighting will be considered when generating images (see constants section).

- **sensitivity="l"**: When synchronize is True, this parameter tells you the sensitivity (or the amount of 'problem') that the output images will show. If the sensitivity is large, any small problem displays will be considered (see constants section).

**RETURN**

None

<a name="datald"></a>

## DATALOADER

The 'dataloader' module has the function of loading the pre-processed data and leaving it ready for use.

**Constants:**

- *data*: Returns information about the loaded data, such as quantity, labels, division, etc.

Methods of the 'data' class:

```
data.training() #returns training data as a tuple: (inputs, labels)
data.validation() #returns validation data as a tuple: (inputs, labels)
data.test() #returns the test data as a tuple: (inputs, labels)
data.items() #returns all data as a tuple: (inputs, labels)
```

*Constant for the image subpackage*

- *image*

### Functions

1. [load](#fd_load)

<a name="fd_load"></a>

### - load(*path_imgs=None*, *tr=None*, *val=None*, *ts=None*, *to_tensor=False*, *transform=None*, *from_mega=False*)

This function loads and separates the data between training, validation and testing. You have the option of returning tensors for use in conjunction with 'pytorch' or returning numpy arrays.

**PARAMETERS**

- **path_imgs=None**: This parameter indicates the location where the images_out folder is. If None, the loader will search the default path.

- **tr=None**: This parameter indicates the percentage (0 to 1) of data that will be used as training (If None, it will be calculated automatically).

- **val=None**: This parameter indicates the percentage (0 to 1) of data that will be used as validation (If None, it will be calculated automatically).

- **ts=None**: This parameter indicates the percentage (0 to 1) of data that will be used as a test (If None, it will be calculated automatically).

- **to_tensor=False**: If True, the function will create the folder structure used in pytorch and return a tuple with the three data sets.

- **transform=None**: If 'to_tensor' is True, this parameter will be used to apply transformations to the images. Case transform for None, a standard transformation will be used:

```
transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor()
])
```

- **from_mega=False**: If True, the function will look for the data in the Mega API, if the data does not exist, it will return an exception (whenever it is set to True, it has to log into the mega before, using the API subpackage).

**RETURN**

There are two possible returns:

If to_tensor is True:

- returns a tuple of size three, containing training_set, validation_set and test_set.

If to_tensor is False:

- returns the constant 'data' with the data information.

<a name="exe"></a>

## Exemples

*Select options

```
preprocess.select(
    [preprocess.oasis, preprocess.liubliana],
    sex = lambda x: x == preprocess.female,
    age = lambda x: 30 < x < 40,
    ms = lambda x: x != preprocess.healthy,
    training = True,
    test = True,
    unknown=False
)
```

*View selected data

```
print(len(preprocess.data.selected_data()))
print(preprocess.data.selected_data()[0])
```

*Preprocessing configuration: to_slice

```
preprocess.define(
    max_imgs=10,
    dim=(),
    center=True,
    synchronize=False,
    format_out="jpg",
    view=preprocess.view.axial,
    weighting=preprocess.weighting.T2,
    sensitivity=preprocess.sensitivity.large
)
```

*Complete example to preprocess the data

```
from imsmri import preprocess
from imsmri.api import mega

import getpass

preprocess.load(
    "/home/wellington/Trabalho/Bolsa/iMRI-Dataset/Databases/Original/Compressed",
    "/home/wellington/Trabalho/Bolsa/iMRI-Dataset/Databases/Pre"
)

mega.login("email", getpass.getpass("[MEGA] password: "), download=True, upload=True)

preprocess.select() #all for default

preprocess.sequence(
    preprocess.functions.register_masks,
    preprocess.functions.register_MNI,
    preprocess.functions.denoise_masks,
    preprocess.functions.skull_strip,
    preprocess.functions.N4,
    preprocess.functions.to_slice,
    upload=False
)

preprocess.run(to=2, init=True)

mega.upload_images_out()
```

*Complete example for using data (local)

```
from imsmri import dataloader

data = dataloader.load(path_imgs="/home/wellington/Trabalho/EM/imsmri/__res/images_out", val=0.5)

print(data)

train = dataloader.data.training()
val = dataloader.data.validation()
test = dataloader.data.test()
```

*Complete example to use the data (from Mega)

```
from imsmri import dataloader
from imsmri.api import mega

import getpass

mega.login("your@email.com", getpass.getpass("password: "), download=True, upload=True)

data = dataloader.load(val=0.5, from_mega=True)

print(data)

train = dataloader.data.training()
val = dataloader.data.validation()
test = dataloader.data.test()
```

<a name="torch"></a>

*Complete example for loading data as tensors

```
from imsmri import dataloader
from imsmri.api import mega

import torch.utils.data as data
import getpass

mega.login("your@email.com", getpass.getpass("password: "), download=True, upload=True)

train_set, val_set, test_set = dataloader.load(val=0.5, to_tensor=True, from_mega=True)

train_loader = data.DataLoader(train_set, batch_size=10, shuffle=True, num_workers=2)
val_loader = data.DataLoader(val_set, batch_size=10, shuffle=True, num_workers=2)
test_loader = data.DataLoader(test_set, batch_size=10, shuffle=True, num_workers=2)

print(dataloader.data)
```

<a name="colab"></a>

## Google Colab

Instructions for using the imsmri package on the Google Colab:

```
!sudo rm -R iMRI-Dataset
!sudo rm -R iMRIDataset
!git clone LINK-REPOSITORY
!mv iMRI-Dataset iMRIDataset

!pip uninstall --yes nibabel
!pip install SimpleITK medpy nibabel==2.1.0 mega.py

from iMRIDataset.imsmri import preprocess
from iMRIDataset.imsmri import dataloader
from iMRIDataset.imsmri.api import mega
```
