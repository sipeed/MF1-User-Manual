#!/bin/bash

function ergodic(){
for file in ` ls $1`
do
    if [ -d $1"/"$file ]
    then
        ergodic $1"/"$file
    else
        local path=$1"/"$file   #得到文件的完整的目录
        local name=$file        #得到文件的名字
        #做自己的工作.
        if [ "${file##*.}" = "bmp" ]; then
            python3 bmp2hex.py $file -kbin

        fi
    fi
done
}

INIT_PATH="."
ergodic $INIT_PATH

#delete exist file
if [ -e pic.kfpkg ]
then
    rm pic.kfpkg
fi

#compress bin to kfpkg
zip pic.kfpkg flash-list.json 0.bin 1.bin 2.bin 3.bin 4.bin 5.bin 6.bin

if [ x"$1" = x1 ]; then 
    echo "merge kfpkg"

    #merge kfpkg to bin
    python3 merge_kfpkg.py pic.kfpkg
    rm pic.kfpkg
    # addr file save_file
    python3 pack_kfpkg.py 12582912 pic.bin pic.kfpkg
fi

rm *.bin
