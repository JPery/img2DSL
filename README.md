# img2DSL

## Usage

- Clone repo with the following command in order to get the [ocl-dataset](https://github.com/tue-mdse/ocl-dataset) dependency

``
git clone --recurse-submodules https://github.com/JPery/img2DSL.git
``
## Installing

In order to ease the installation of all requirements and dependencies we've created an ``install.sh`` file.

But you can install this requirements and dependencies on your own:

### Requirements

- Ubuntu >= 18.04
- Java >= 1.8
- Python >= 3.6
- [USE Tool](https://sourceforge.net/projects/useocl/) == 5.2.0 (You have to download and extract it into the project root folder)
- [Tesseract](https://github.com/tesseract-ocr/tesseract/releases/tag/4.1.1) == 4.1.1, [Tesseract Training Tools](https://tesseract-ocr.github.io/tessdoc/Compiling-%E2%80%93-GitInstallation.html#build-with-training-tools) and the [Tesseract eng language](https://github.com/tesseract-ocr/tessdata_best/raw/master/eng.traineddata) from the [tessdata_best repository](https://github.com/tesseract-ocr/tessdata_best).


### Installing Python dependencies

``
pip3 install -r requirements.txt
``



## Running

To re-run the experiments that we present in our paper [1], run the process.sh script:

``
./process.sh
``


# Citation

[1] Jorge Perianez, Roberto Rodriguez-Echeverria, Loli Burgueño, Jordi Cabot. Towards the Optical Character Recognition of DSLs. In Proc. of the ACM SIGPLAN International Conference on Software Language Engineering (SLE'20). 2020. To appear.
