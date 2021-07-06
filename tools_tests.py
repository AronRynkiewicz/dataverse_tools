import unittest
import ast
import os
from tools import *

# python -m unittest tools_tests.py

class TestTools(unittest.TestCase):
    api = None
    online_dataset = None
    dataset_to_be_created = None
    dummy_dataset = None

    def setUp(self):
        os.chdir('files')
        self.api = NativeApi(MXRDR_PATH, API_TOKEN)
        self.online_dataset = read_from_file('dataset.json')
        self.dataset_to_be_created = 'test_dataset.json'
        self.dummy_dataset = 'dummy_dataset.json'

    def test_check_connection(self):
        self.assertEqual(200, check_connection(self.api))
    
    def test_get_datasets_metadata(self):
        self.assertEqual(
            self.online_dataset['datasetVersion']['metadataBlocks'],
            get_datasets_metadata(self.api, 'doi:10.21989/FK2/CRVEJO')['metadataBlocks']
        )
    
    def test_get_macromolecular_metadata(self):
        self.assertEqual(
            self.online_dataset['datasetVersion']['metadataBlocks']['macromolecularcrystallography'],
            get_macromolecular_metadata(self.api, 'doi:10.21989/FK2/CRVEJO')
        )
    
    def test_get_dataset_id(self):
        self.assertEqual(
            115024,
            get_dataset_id(self.api, 'doi:10.21989/FK2/CRVEJO')
        )
    
    def test_create_dataset(self):
        data = ast.literal_eval(create_dataset(self.dataset_to_be_created).stdout.decode("UTF-8"))
        self.assertEqual('OK', data['status'])
        self.assertEqual(
            get_dataset_id(self.api, data['data']['persistentId']),
            data['data']['id']
        )
        self.assertEqual(
            get_datasets_metadata(self.api, data['data']['persistentId'])['metadataBlocks'],
            read_from_file(self.dataset_to_be_created)['datasetVersion']['metadataBlocks']
        )
        delete_draft_dataset(data['data']['id'])
    
    def test_delete_draft_dataset(self):
        data = ast.literal_eval(create_dataset(self.dummy_dataset).stdout.decode("UTF-8"))
        id = get_dataset_id(self.api, data['data']['persistentId'])
        self.assertEqual(
            200,
            delete_draft_dataset(id)
        )
        self.assertEqual(-1, get_dataset_id(self.api, data['data']['persistentId']))

    def tearDown(self):
        os.chdir('..')

if __name__ == '__main__':
    unittest.main()