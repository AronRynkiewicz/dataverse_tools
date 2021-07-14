# Dataverse tools
[MX-RDR](https://mxrdr.icm.edu.pl/) tool, in form of python script, which simplifies new data set creation.

# Installation
To use this tool, you need:
* Python 3

we also suggest:
* git - for easier download
* virtual environment (eg. anaconda) - for packages management

Using terminal just paste:
```
git clone https://github.com/AronRynkiewicz/dataverse_tools
```
to download this tool.

Next change directory to dataverse_tools and paste:
```
pip install -r requirements.txt
```
to install required python packages.

Last step is pasting your API token to credentials.py file between '':
```
API = {
    'LOGIN_DATA' : {
        'username': '',
        'password': '',
    },

    'API_TOKEN': 'you api token goes here',
}
```

# Usage
To use script write:
```
python main.py -f dataset_metadata.json -d data_directory -fp common_file_prefix
```
while being in dataverse_tools directory.

Flags meaning:
* f - metadata for new dataset in form of json file.
* d - directory where script will look for data.
* fp - Common prefix for all files to be uploaded. Notice that script expects that file id will be separated by _ from common prefix, eg.: file_0001.txt file_0002.txt.
