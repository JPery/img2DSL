#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Usage $0 out_folder_name font_path"
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
python3.7 recognize_text_from_image.py $1
python3.7 comparate_expressions_with_recognized_text.py $1
python3.7 ratio_histogram.py $1