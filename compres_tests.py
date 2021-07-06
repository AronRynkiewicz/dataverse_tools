import unittest
import shutil
from compres import *

NUMBER_OF_FILES = 3500
DUMMY_DIR_NAME = 'folder'
DATASET_NAME = '16S_D31-cyt180j_1'
TEST_ZIP_NAME = 'test'


def create_dummy_dir():
        os.mkdir(DUMMY_DIR_NAME)


def create_dummy_files(number_files):
    """
    Creates test files.

    Parameters
    ----------
    number_files : int
        Number of test files.

    """
    os.chdir(DUMMY_DIR_NAME)
    for i in range(0, number_files):
        file_name = DATASET_NAME + '_data_' + str(i) + '.h5'
        with open(file_name, 'w') as file:
            lines = ['pierwsza\n', 'druga\n', 'trzecia\n']
            file.writelines(lines)
    os.chdir('..')


class TestCompres(unittest.TestCase):

    def setUp(self):
        create_dummy_dir()
        create_dummy_files(NUMBER_OF_FILES)
    
    def test_zip_creation(self):
        checkZip(DUMMY_DIR_NAME, TEST_ZIP_NAME, DATASET_NAME)
        dirs_count = len([file for file in os.listdir() if file.startswith(TEST_ZIP_NAME) and file.endswith('.zip')])
        self.assertEqual(math.ceil(NUMBER_OF_FILES / LIMIT), dirs_count)

    def tearDown(self):
        shutil.rmtree(DUMMY_DIR_NAME)

        for i in range(math.ceil(NUMBER_OF_FILES / LIMIT)):
            os.remove(TEST_ZIP_NAME + str(i) + '.zip')


if __name__ == '__main__':
    unittest.main()
