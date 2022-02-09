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
python main.py -at API_TOKEN -f dataset_metadata.json -d data_directory -fp common_file_prefix -u DOI -m mode
```
while being in dataverse_tools directory.

Flags meaning:
* at - your api token from [MX-RDR](https://mxrdr.icm.edu.pl/) (obligatory).
* d - directory where script will look for data (obligatory).
* fp - Common prefix for all files to be uploaded. Notice that script expects that file id will be separated by _ from common prefix, eg.: file_0001.txt file_0002.txt (obligatory).
* f - metadata for new dataset in form of json file (optional).
* u - DOI for given dataset, to which files will be send (optional) Important note: all our DOIs begin with doi:10.18150 so You need to pass just part after "/" sign, e.g.: doi:10.18150/ABCDEF just write ABCDEF.
* m - mode, you can use this script in three diffrent ways (optional, script by default zips files and asks user for next steps):
    * send - zipps and sends files to given dataset (requires -u flag),
    * zip - only zips files in given directory (default behaviour),
    * create - creates new dataset, zips files and sends them (requires -f flag).

# Examples
Short command:
```console
python main.py -at abcdefqwe-adrf-axdrrg-dwqzd-11qwe -d images -fp img
```

Send mode example:
```console
python main.py -at abcdefqwe-adrf-axdrrg-dwqzd-11qwe -d images -fp img -u AAAAA -m send
```

Zip mode example:
```console
python main.py -at abcdefqwe-adrf-axdrrg-dwqzd-11qwe -d images -fp img -m zip
```

Create mode example:
```console
python main.py -at abcdefqwe-adrf-axdrrg-dwqzd-11qwe -d images -fp img -m create -f my_images_metadata.json
```
