import unittest
import ast
import os
from compres import *

# python -m unittest tools_tests.py
# create an empty folder named "folder"

class TestTools(unittest.TestCase):
    lst_zip = None
    lst_zip2 = None
    number_files = None


    def setUp(self):
        self.lst_zip = ['nowyDir0.zip','nowyDir1.zip','nowyDir2.zip']
        self.lst_zip2 = ['nowyDir0.zip', 'nowyDir1.zip', 'nowyDir2.zip','nowyDir3.zip','nowyDir4.zip','nowyDir5.zip','nowyDir6.zip',
                         'nowyDir7.zip','nowyDir8.zip','nowyDir9.zip','nowyDir10.zip','nowyDir11.zip']
        self.number_files = 2000
        self.number_files2 = 10000


    def test_check_dummy_zip(self):
        self.assertEqual(True,check_dummy_zip(self.lst_zip, self.number_files))

    def test_check_dummy_zip2(self):
         self.assertEqual(True, check_dummy_zip(self.lst_zip2, self.number_files2))

if __name__ == '__main__':
    unittest.main()