# Path SubPackage

This subpackage provides functions for handling system-wide directories. This package has some functions that are also present in the standard 'os' package.

## Variables

Directories used by the system:

- *files_zip*
- *files_unzip*
- *files_pre*
- *files_out*
- *mega_source*

## Constants

Constant directories used by the system:

- *json_file*
- *temp_file*
- *images_file*
- *log_file*

## Functions

- verify(*path*)
- join(**args*)
- dirname(*path*)
- isfile(*path*)
- isdir(*path*)
- lastname(*path*)
- remove(*path*)
- change(*path1*, *path2*, *path_root*, *ini=True*, *end=False*)
- diference(*path_b*, *path_s*)
- mkdirs(*data*, *pre=False*, *unzip=False*)