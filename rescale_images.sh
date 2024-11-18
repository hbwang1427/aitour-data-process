#!/bin/sh
list_file=$1
output_dir=$2
base_dir='/home/pangolins/work/data/'

while IFS=$'\n' read -r img; do
    ext="${img##*.}"
    src_file=$base_dir"${img%.*}".${ext}
    tgt_file=$base_dir"${img%.*}"_small.${ext}
#    echo $tgt_file
#    echo $src_file
    \rm -f "${tgt_file}"
    if [ ! -f "${tgt_file}" ]; then 
echo     ffmpeg -i \"${src_file}\" -vf scale=-1:200 \"${tgt_file}\"
    fi
done < "${list_file}"

# Explicitly report array content.
#i=0
#while (( ${#img_list[@]} > i )); do
#    i=$((i+1))
#    printf "${img_list[$i]}\n"
#done

exit
for img in `cat $img_list`; do
#    fname=`basename $img`
    ext="${img##*.}"
    src_file=$base_dir"${img%.*}".${ext}
    tgt_file=$base_dir"${img%.*}"_small.${ext}
#    echo $src_file
    if [ ! -f "$tgt_file" ]; then 
        echo "$src_file"
#        ffmpeg -i "$src_file" -vf scale=-1:100 "$tgt_file"
    fi
#    exit
done
