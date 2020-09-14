#!/usr/bin/env bash
if [ "$#" -ne 4 ]; then
    echo "Usage $0 out_folder_name font_path tesseract_lang recognize_file"
    exit
fi
if [ ! -f "$2" ]; then
    echo "font_path '$2' does not exist"
    exit
fi
echo "Using font '$1'"
mkdir -p $1
mkdir -p $1/images
python3 generate_image_from_expressions.py $1 $2
mkdir -p $1/recognized_text
python3 $4.py $1 $3
echo "Comparating expressions with recognized text"
python3 comparate_expressions_with_recognized_text.py $1
python3 parseUse_v2.py $1
