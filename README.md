# img2DSL

## About
img2DSL is an image recognition toolkit designed to study how Optical Character Recognition can be applied to images that contain DSL snippets.
Using the Object Constraint Language (OCL) as an example of textual DSL and given a dataset of Ecore models (and its OCL expressions), this toolkit encodes the OCL expressions into images and tests how different strategies improve the default OCR quality. In this project we use Tesseract as OCR engine and the different strategies are different OCR models and custom algorithms.

In order to evaluate the toolkit and the quality of its different strategies, we load the recognized expressions in the USE tool to measure of how many expressions are valid after the recognition.

## Usage

- Clone repo with the following command in order to get the [ocl-dataset](https://github.com/tue-mdse/ocl-dataset) dependency

``
git clone --recurse-submodules https://github.com/JPery/img2DSL.git
``
## Installing

In order to ease the installation of all requirements and dependencies we've created an ``install.sh`` file.

You should run ``apt-get update`` in order to update repositories before running the script.

You can also install this requirements and dependencies on your own:

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

To run the experiments with the OCL [dataset](https://ieeexplore.ieee.org/document/7962414) by Noten et al., execute the process.sh script:

``
./process.sh
``

The estimated time to run the full experiment is 5 hours in an AMD Ryzen 9 3900X CPU with 32GB of RAM and a 512GB NVMe SSD disk in Ubuntu 20.04.

Note that the master branch contains the full OCL [dataset](https://ieeexplore.ieee.org/document/7962414), which contains expressions that were not valid for our approach hence we did not use them in our paper [1]. To re-run the exact experiments that we present in our paper [1], please move to the branch SLE20-artifact.

# Citation

[1] Jorge Perianez-Pascual, Roberto Rodriguez-Echeverria, Loli Burgueño, and Jordi Cabot. 2020. Towards the Optical Character Recognition of DSLs. In Proceedings of the 13th ACM SIGPLAN International Conference on Software Language Engineering (SLE ’20), November 16–17, 2020, Virtual, USA. ACM, New York, NY, USA, 7 pages. https://doi.org/10.1145/3426425.3426937

