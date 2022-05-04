# MEGA SubPackage

This API was created with the intention of sharing pre-processed files with other people or other services, such as google colab. This subpackage contains functions to download and upload files to the Mega in a simple and practical way.

## Functions

- login(*email*, *passwd*, *download=False*, *upload=False*)
- upload_folder(*path_folder*)

NOTE: When using the login function with download in true, the system will automatically search for the compressed files of the Mega. If you do not want the automatic download, log in only as an upload.