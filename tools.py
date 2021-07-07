from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.models import Datafile
import json
import requests
import subprocess as sp
from credentials import API

API_TOKEN = API['API_TOKEN']

MXRDR_PATH = 'https://{}:{}@mxrdr-test.icm.edu.pl'.format(
    API['LOGIN_DATA']['username'],
    API['LOGIN_DATA']['password'],
)


def check_connection(api):
    """
    Checks if connection to MXRDR can be established.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    
    Returns
    -------
    HTML response status code
        When connection is succesful returns 200, otherwise 400ish code.
    """
    resp = api.get_info_version()
    return resp.status_code


def create_dataset(json_file, dataverse='root'):
    """
    Creates datasets in given dataverse.

    Parameters
    ----------
    json_file : JSON object (dict)
        File from which dataset will be created.
    dataverse : str
        Name of dataverse. Default is root.
    
    Returns
    -------
    bool
        True if dataset has been created, otherwise - False.
    """

    shell_command = 'curl -H "X-Dataverse-key:{0}" '.format(API_TOKEN)
    shell_command += '-X POST {0}/api/dataverses/{1}/datasets '.format(MXRDR_PATH, dataverse)
    shell_command += '--upload-file {0}'.format(json_file)
  
    return sp.run(shell_command, shell=True, stdout=sp.PIPE)


def save_to_file(file_name, data):
    """
    Saves JSON object to file. 
    
    JSON object such as datasets metadata, macromolecular metadata.

    Parameters
    ----------
    file_name : str
        Name of file to write data.
    data : JSON object (dict)
        Data in JSON format. 
    """
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def read_from_file(file_name):
    """
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
    """
    with open(file_name, 'r') as file:
        data = json.load(file)
    
    return data


def get_macromolecular_metadata(api, DOI):
    """
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
    """
    data_api = DataAccessApi(MXRDR_PATH)
    dataset = api.get_dataset(DOI)
    macromolecular_metadata = dataset.json()['data']['latestVersion']['metadataBlocks']['macromolecularcrystallography']
    return macromolecular_metadata


def get_datasets_metadata(api, DOI):
    """
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
    """
    data_api = DataAccessApi(MXRDR_PATH)
    dataset = api.get_dataset(DOI)
    metadata = dataset.json()['data']['latestVersion']
    return metadata


def update_metadata(DOI, json_file):
    """
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
    """
    file = read_from_file(json_file)

    shell_command = 'curl -H "X-Dataverse-key:{0}" '.format(API_TOKEN)
    shell_command += '-X PUT {0}/api/datasets/:persistentId/versions/:draft?persistentId={1} '.format(MXRDR_PATH, DOI)
    shell_command += '-F "jsonData={0}"'.format(file)

    try:
        sp.run(shell_command, shell=True, stdout=sp.PIPE)
    except Exception:
        return False
    return True


def upload_file_to_dataset(DOI, file_name, file_description):
    """
    Uploads single file to dataset.

    Parameters
    ----------
    DOI : str
        DOI of dataset to which file will be uploaded.
    file_name : str
        Name of file to upload.
    file_description : str
        Description of uploaded file.
    
    Returns
    -------
    HTML response status code
        When upload is succesful returns 200, otherwise 400ish code.
    """
    params = dict(
        description=file_description,
        termsOfUseAndAccess=dict(
            termsType='LICENSE_BASED',
            license='CC BY Creative Commons Attribution License 4.0',
        )
    )

    params_as_json_string = json.dumps(params)

    payload = dict(jsonData=params_as_json_string)

    url_dataset_id = '{0}/api/datasets/:persistentId/add?persistentId={1}&key={2}'.format(MXRDR_PATH, DOI, API_TOKEN)

    files = {'file': (file_name, open(file_name, 'rb'))}

    r = requests.post(url_dataset_id, data=payload, files=files)
    return r.status_code


def get_license_info():
    """
    Prints available licenses. 
    """
    print(requests.get(MXRDR_PATH + '/api/info/activeLicenses').json()['data']['message'])


def get_dataset_id(api, DOI):
    """
    Gets dataset ID by dataset DOI.

    Parameters
    ----------
    api : pyDataverse object
        Object of pyDataverse NativeApi class.
    DOI : str
        DOI of a dataset.
    
    Returns
    -------
    id
        ID of given dataset which is int or -1 if given dataset does not exists.
    """
    data_api = DataAccessApi(MXRDR_PATH)
    try:
        dataset = api.get_dataset(DOI)
    except Exception:
        return -1

    id = dataset.json()['data']['id']
    return id


def delete_draft_dataset(id):
    """
    Deletes draft of given dataset.

    Parameters
    ----------
    id : int
        ID of dataset's draft to be deleted.
    
    Returns
    -------
    HTML response status code
        When upload is succesful returns 200, otherwise 400ish code.
    """
    r = requests.delete(MXRDR_PATH + '/api/datasets/{0}/versions/:draft?key={1}'.format(id, API_TOKEN))
    return r.status_code

