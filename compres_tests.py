import unittest
import shutil
import sys
from compres import *

# python -m unittest compres_tests.py

NUMBER_OF_FILES = 6500
DUMMY_DIR_NAME = "folder3"
UNZIPPED_DIR_NAME = "folder_unzip3"
DATASET_NAME = "16S_D31-cyt180j_1"
TEST_ZIP_NAME = "test"

PATH_DICT = {
    "win32": "\\",
    "linux": "/",
    "darwin": "/",
}


def create_dummy_dir(dir_name):
    os.mkdir(dir_name)


def create_dummy_files(number_files):
    """
    Creates test files.

    Parameters
    ----------
    number_files : int
        Number of test files.

    """
    os.chdir(DUMMY_DIR_NAME)
    lst = []
    for i in range(0, number_files):
        file_name = DATASET_NAME + "_data_" + str(i) + ".h5"
        with open(file_name, "w") as file:
            lines = ["pierwsza\n", "druga\n", "trzecia\n"]
            file.writelines(lines)
        lst.append(file_name)
    os.chdir("..")
    return lst


def unzipFile(lst_files):
    for i in lst_files:
        with ZipFile(".." + PATH_DICT[sys.platform] + i, "r") as zipObj:
            zipObj.extractall()


class TestCompres(unittest.TestCase):
    files_lst = []

    def setUp(self):
        create_dummy_dir(DUMMY_DIR_NAME)
        create_dummy_dir(UNZIPPED_DIR_NAME)
        create_dummy_files(NUMBER_OF_FILES)
        self.files_lst = zip_files(DUMMY_DIR_NAME, TEST_ZIP_NAME, DATASET_NAME)

    def test_zip_creation(self):
        dirs_count = len(
            [
                file
                for file in os.listdir()
                if file.startswith(TEST_ZIP_NAME) and file.endswith(".zip")
            ]
        )
        self.assertEqual(len(self.files_lst), dirs_count)

    def test_filenames(self):
        os.chdir(UNZIPPED_DIR_NAME)
        unzipFile(self.files_lst)
        file_count = len(
            [
                file
                for file in os.listdir()
                if file.startswith(DATASET_NAME) and file.endswith(".h5")
            ]
        )
        self.assertEqual(NUMBER_OF_FILES, file_count)
        os.chdir("..")

    def tearDown(self):
        shutil.rmtree(DUMMY_DIR_NAME)
        shutil.rmtree(UNZIPPED_DIR_NAME)

        for file in self.files_lst:
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
