from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.models import Datafile
import json
import subprocess as sp
from credentials import API

API_TOKEN = API['API_TOKEN']

MXRDR_PATH = 'https://{}:{}@mxrdr-test.icm.edu.pl'.format(
    API['LOGIN_DATA']['username'],
    API['LOGIN_DATA']['password'],
)


def check_connection(api):
    '''
    Checks if connection to MXRDR can be established.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    
    Returns
    -------
    HTML response status code
        When connection is succesful returns 200, otherwise 400ish code.
    '''
    resp = api.get_info_version()
    return resp.status_code


def create_dataset(api, json_file, dataverse='root'):
    '''
    Creates datasets in given dataverse.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    json_file : JSON object (dict)
        File from which dataset will be created.
    dataverse : str
        Name of dataverse. Default is root.
    
    Returns
    -------
    bool
        True if dataset has been created, otherwise - False.
    '''
    ds = Dataset()
    ds.from_json(read_file(json_file))
    if ds.validate_json():
        try:
            resp = api.create_dataset(dataverse, ds.json())
            return True
        except Exception:
            return False
    
    return False


def save_to_file(file_name, data):
    '''
    Saves JSON object to file. 
    
    JSON object such as datasets metadata, macromolecular metadata.

    Parameters
    ----------
    file_name : str
        Name of file to write data.
    data : JSON object (dict)
        Data in JSON format. 
    '''
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def read_from_file(file_name):
    '''
    Reads JSON object from file. 
    
    JSON object such as datasets metadata, macromolecular metadata.

    Parameters
    ----------
    file_name : str
        Name of file to read data.
    
    Returns
    -------
    JSON object (dict)
        Returns read data.
    '''
    with open(file_name, 'r') as file:
        data = json.load(file)
    
    return data


def get_macromolecular_metadata(api, DOI):
    '''
    Gets macromolecular metadata of given dataset.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    DOI : str
        DOI of dataset from which metadata will be collected.
    
    Returns
    -------
    JSON object (dict)
        Returns macromolecular metadata in JSON format.
    '''
    data_api = DataAccessApi(MXRDR_PATH)
    dataset = api.get_dataset(DOI)
    macromolecular_metadata = dataset.json()['data']['latestVersion']['metadataBlocks']['macromolecularcrystallography']
    return macromolecular_metadata


def get_datasets_metadata(api, DOI):
    '''
    Gets whole metadata of given dataset.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    DOI : str
        DOI of dataset from which metadata will be collected.
    
    Returns
    -------
    JSON object (dict)
        Returns metadata in JSON format.
    '''
    data_api = DataAccessApi(MXRDR_PATH)
    dataset = api.get_dataset(DOI)
    metadata = dataset.json()['data']['latestVersion']
    return metadata


def update_metadata(DOI, json_file):
    '''
    Updates metadata of given datasets.

    Parameters
    ----------
    DOI : str
        DOI of dataset from which metadata will be collected.
    json_file : str
        Name of file which contains updated metadata.
    
    Returns
    -------
    bool
        Return True if metadata was successfully sent to database, otherwise - False.
    '''
    file = read_from_file(json_file)

    shell_command = 'curl -H "X-Dataverse-key: {0}" '.format(API_TOKEN)
    shell_command += '-X PUT {0}/api/datasets/:persistentId/versions/:draft?persistentId={1} '.format(MXRDR_PATH, DOI)
    shell_command += '-F "jsonData={0}"'.format(file)

    try:
        sp.run(shell_command, shell=True, stdout=sp.PIPE)
    except Exception:
        return False
    return True


def upload_file_to_dataset(api, DOI, file_name):
    df = Datafile()
    df.set({"pid": DOI, "filename": file_name})
    try:
        resp = api.upload_datafile(DOI, file_name, df.json())
        return True
    except Exception:
        return False


def wrapper(data):
    d = {}
    d['datasetVersion'] = data
    return d


api = NativeApi(MXRDR_PATH, API_TOKEN)
print(check_connection(api))

# data = read_from_file('dataset.json')
# data = wrapper(data)
# save_to_file('dataset.json', data)
# print(create_dataset(api, 'dataset.json'))

# macromolecular_metadata = get_macromolecular_metadata(api, 'doi:10.21989/FK2/54VA1F')
# save_to_file('metadata.json', macromolecular_metadata)


# print(update_metadata('doi:10.21989/FK2/3AONMG', 'metadata.json'))


# macromolecular_metadata = get_datasets_metadata(api, 'doi:10.21989/FK2/54VA1F')
# save_to_file('dataset.json', macromolecular_metadata)


# print(upload_file_to_dataset(api, 'doi:10.21989/FK2/A5ZCKW', 'dataset.json'))


