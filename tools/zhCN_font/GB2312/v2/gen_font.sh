#!/bin/bash

zip font.kfpkg flash-list.json GB2312_16x16.FON GB2312_24x24.FON GB2312_32x32.FON

python3 merge_kfpkg.py font.kfpkg
rm font.kfpkg

python3 pack_kfpkg.py 1048576 font.bin font.kfpkg
rm font.bin