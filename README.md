# simple-binarization
Simple binarization based on Otsu

## install
```
virtualenv -p python3 venv # generate once the virtal environment for Python
source venv/bin/activate # activate virtual environment
pip install -r tmp/requirements.txt # install once the required python packages
 ```
## run
You can run `binarize.py` directly on the image or call `run.sh`, which gets a pdf image as input, creates an `out` folder and runs pdfimages to extract jpg files. On each of those, binarize.py is applied:

* `binarize.py <image.jpg> -o <outdir>`
* or `run.sh <images.pdf>`
