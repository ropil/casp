casp
====

CASP target download utility.

*Depends*;

- python 3.6 and
- BeautifulSoup4

## Installation
Downloading and setting up venv

```bash
git clone https://github.com/ropil/casp;
cd casp;
python -m venv venv;
source venv/bin/activate;
pip install beautifulsoup4;
deactivate;
```

## Running

```bash
DOWNLOAD_DIRECTORY=./;
PATH_TO_CASP_UTILS=./;
mkdir -p ${DOWNLOAD_DIRECTORY};
source ${PATH_TO_CASP_UTILS}/venv/bin/activate;
${PATH_TO_CASP_UTILS}/casp_download_targets.py ${DOWNLOAD_DIRECTORY} -verbose;
```
