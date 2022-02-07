# Dataverse tools
[MX-RDR](https://mxrdr.icm.edu.pl/) tool, in form of python script, which simplifies new data set creation.

# Available functionality
Using just one script you can:
* create new dataset
* add metadata to it
* zip all files and add them to dataset
<!--- * add JPEG file from first diffraction image --->

# Installation
To use this tool, you need:
* Python 3
<!--- * [adxv](https://www.scripps.edu/tainer/arvai/adxv.html) - for diffraction image creation --->

we also suggest:
* git - for easier download
* virtual environment (eg. anaconda) - for packages management

Using terminal just paste:
```console
git clone https://github.com/AronRynkiewicz/dataverse_tools
```
to download this tool.

Next change directory to dataverse_tools and paste:
```console
pip install -r requirements.txt
```
to install required python packages.

# Usage
To use script write:
```console
python main.py -at API_TOKEN -f dataset_metadata.json -d data_directory -fp common_file_prefix -u URL -m mode
```
while being in dataverse_tools directory.

Flags meaning:
* at - your api token form [MX-RDR](https://mxrdr.icm.edu.pl/) (obligatory).
* f - metadata for new dataset in form of json file (optional).
* d - directory where script will look for data (obligatory).
* fp - Common prefix for all files to be uploaded. Notice that script expects that file id will be separated by _ from common prefix, eg.: file_0001.txt file_0002.txt (obligatory).
* u - URL for given dataset, to which files will be send (optional).
* m - mode, you can use this script in three diffrent ways:
    * send - zipps and sends files to given dataset (requires -u flag),
    * zip - only zips files in given directory,
    * create - creates new dataset, zips files and sends them (requires -f flag).
