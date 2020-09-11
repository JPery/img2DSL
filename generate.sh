#!/usr/bin/env bash
if [ "$#" -ne 4 ]; then
    echo "Usage $0 out_folder_name font_path tesseract_lang recognize_file"
    exit
fi
if [ ! -f "$2" ]; then
    echo "font_path '$2' does not exist"
    exit
fi
mkdir $1
mkdir $1/images
python3.7 generate_image_from_expressions.py $1 $2
mkdir $1/recognized_text
python3.7 $4.py $1 $3
#python3.7 recognize_text_from_image_dlpd.py $1
#python3.7 recognize_text_from_image_repairing.py $1 $3
python3.7 comparate_expressions_with_recognized_text.py $1
python3.7 parseUse_v2.py $1
#python3.7 ratio_histogram.py $1
