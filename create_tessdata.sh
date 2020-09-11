#!/usr/bin/env bash
mkdir traineddat_backup$1
combine_tessdata -u /usr/local/share/tessdata/eng2.traineddata traineddat_backup$1/ocl$1. 2> /dev/null
wordlist2dawg wordlistfile$1 ocl$1.lstm-word-dawg traineddat_backup$1/ocl$1.lstm-unicharset 2> /dev/null
rm traineddat_backup$1/*word-dawg
mv ocl$1.lstm-word-dawg traineddat_backup$1/
cp traineddat_backup$1/ocl$1.lstm-word-dawg traineddat_backup$1/ocl$1.word-dawg
cp ocl.lstm-punc-dawg traineddat_backup$1/ocl$1.lstm-punc-dawg
cp ocl.lstm-punc-dawg traineddat_backup$1/ocl$1.punc-dawg
cd traineddat_backup$1
combine_tessdata ocl$1. 2> /dev/null
cp ocl$1.traineddata /usr/local/share/tessdata/ocl$1.traineddata
cd ..
rm -rf traineddat_backup$1
rm wordlistfile$1