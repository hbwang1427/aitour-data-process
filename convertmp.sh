#!/bin/sh
list_file=$1
base_dir='/home/pangolins/work/data/'

while IFS=$'\n' read -r img; do
    ext="${img##*.}"
    src_file=$base_dir"${img%.*}".wav
    tgt_file=$base_dir"${img%.*}".mp3
#    echo $tgt_file
#    echo $src_file
    \rm -f "${tgt_file}"
    if [ -f "${src_file}" ]; then 
echo       ffmpeg -i \"${src_file}\" \"${tgt_file}\"
    fi
done < "${list_file}"

