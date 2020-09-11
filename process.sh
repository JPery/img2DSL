#!/usr/bin/env bash
echo "Converting ecores to JSON file..."
python3 parseEcores.py
echo "Loading exprssions into USE... (this will take a while)"
python3 parseUse.py

echo "Creating default_punct model"
mkdir default_punct
combine_tessdata -u /usr/local/share/tessdata/eng.traineddata default_punct/default_punct. 2> /dev/null
cp ocl.lstm-punc-dawg default_punct/default_punct.lstm-punc-dawg
cp ocl.lstm-punc-dawg default_punct/default_punct.punc-dawg
cd default_punct
combine_tessdata default_punct. 2> /dev/null
cp default_punct.traineddata /usr/local/share/tessdata/default_punct.traineddata
cd ..
rm -rf default_punct
echo "Created"

echo "Creating default_punct_lang model"
mkdir default_punct_lang
combine_tessdata -u /usr/local/share/tessdata/eng.traineddata default_punct_lang/default_punct_lang. 2> /dev/null
wordlist2dawg wordlistfile default_punct_lang.lstm-word-dawg default_punct_lang/default_punct_lang.lstm-unicharset 2> /dev/null
rm default_punct_lang/*word-dawg
mv default_punct_lang.lstm-word-dawg default_punct_lang/
cp default_punct_lang/default_punct_lang.lstm-word-dawg default_punct_lang/default_punct_lang.word-dawg
cp ocl.lstm-punc-dawg default_punct_lang/default_punct_lang.lstm-punc-dawg
cp ocl.lstm-punc-dawg default_punct_lang/default_punct_lang.punc-dawg
cd default_punct_lang
combine_tessdata default_punct_lang. 2> /dev/null
cp default_punct_lang.traineddata /usr/local/share/tessdata/default_punct_lang.traineddata
cd ..
rm -rf default_punct_lang
echo "Created"

echo "Processing images with default model"
./full_process.sh eng recognize_text_from_image
echo "Processing images with default_punct model"
./full_process.sh default_punct recognize_text_from_image
echo "Processing images with default_punct_lang model"
./full_process.sh default_punct_lang recognize_text_from_image
echo "Processing images with default_punct_lang_domain model"
./full_process.sh eng recognize_text_from_image_dlpd
echo "Processing images with repairing model"
./full_process.sh eng recognize_text_from_image_repairing
echo "DONE"
