#!/bin/bash
sudo apt-get install -y libicu-dev libpango1.0-dev libcairo2-dev make g++ autoconf automake libtool pkg-config libpng-dev libjpeg8-dev libtiff5-dev zlib1g-dev libleptonica-dev git python3-virtualenv python3-pip openjdk-8-jre
wget https://github.com/tesseract-ocr/tesseract/archive/4.1.1.tar.gz
tar -zxvf 4.1.1.tar.gz
rm 4.1.1.tar.gz
cd tesseract-4.1.1/
./autogen.sh
./configure
make -j$(nproc)
sudo make install
sudo ldconfig
make -j$(nproc) training
sudo make training-install
cd ..
rm -rf tesseract-4.1.1/
wget "https://github.com/tesseract-ocr/tessdata_best/raw/master/eng.traineddata"
sudo chown -R $(whoami) /usr/local/share/tessdata/
mv eng.traineddata /usr/local/share/tessdata/
virtualenv env --python=python3
source env/bin/activate
pip install -r requirements.txt
wget "https://downloads.sourceforge.net/project/useocl/USE/5.2.x/use-5.2.0.tar.gz?r=https://sourceforge.net/projects/useocl/&ts=$(date +%s%N | cut -b1-10)&use_mirror=master" -O use-5.2.0.tar.gz
tar -zxvf use-5.2.0.tar.gz
rm use-5.2.0.tar.gz