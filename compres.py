import math
from zipfile import ZipFile
import os
from os.path import basename
LIMIT=900

def createDir(dirName):
   """
    Creates a dictionary with filenames.

    :param dirName: string
    The name of the directory where the desired files are located.

    :return: Dictionary

   """
   d={}
   for folderName, subfolders, filenames in os.walk(dirName):
       for filename in filenames:
           if 'data' in filename:
               f = '_'.join(filename.split('_')[:-2])
           else:
               f = '_'.join(filename.split('_')[:-1])
           try:
               d[f].append(filename)
           except Exception:
               d[f] = [filename]

   return d



def zipFilesInDir2(dirName, zipFileName, filter, d, low_range, high_range):
    """
    Creates a compressed files.

    Parameters
    ----------
    dirName : string
    The name of the directory where the desired files are located.

    zipFileName: string
    The name of the compressed file.

    filter: string
    The proper name of the data set.

    d : dictionary
    Dictionary with filenames

    low_range: int
    The number of the first saved file.

    high_range:int
    Last saved file number.

    Returns
    -------
    Compressed files.
    """
    with ZipFile(zipFileName, 'w') as zipObj:
        for key in d:
            for n in filter.split(','):
                if (key == n):
                    for i in range(low_range, high_range):
                        filePath = os.path.join(dirName, d[n][i])
                        zipObj.write(filePath, basename(filePath))
    zipObj.close()


def checkZip(dirName, zipFileName, filter):
    """
    Check the number of files.

    Parameters
    ----------
    dirName : string
    The name of the directory where the desired files are located.

    zipFileName: string
    The name of the compressed file.

    filter: string
    The proper name of the data set.

    """
    d = createDir(dirName)
    for key in d:
        for n in filter.split(','):
            if (key == n):
                temp = int(len(d[key]))
                if (temp < LIMIT):
                    zipFilesInDir2(dirName, zipFileName + '.zip', filter, d, 0, len(d[key]))
                else:
                    number = math.ceil(int(temp) / LIMIT)
                    for i in range(0, int(number)):
                        previous_value = temp
                        temp = temp - LIMIT
                        if temp > 0:
                            zipFilesInDir2(dirName, zipFileName + str(i) + '.zip', filter, d, LIMIT * i, (i+1)*LIMIT)
                        if temp < 0:
                            zipFilesInDir2(dirName, zipFileName + str(i) + '.zip', filter, d, LIMIT * i, (LIMIT * i) + previous_value)


def dummy_files(number_files):
    """
    Creates test files.

    Parameters
    ----------
    number_files int
    Number of test files.

    """
    os.chdir('folder')
    for i in range(0, number_files):
        string='16S_D31-cyt180j_1_data_'+ str(i) +'.h5'
        with open(string, 'w') as f:
            lines = ['pierwsza\n', 'druga\n', 'trzecia\n']
            f.writelines(lines)


def delete_dummy_files(lista_zipow,number_files):
    """
    Deletes test files.

    Parameters
    ----------
    lista_zipow : list
    Compressed files list.

    number_files: int
    Number of files generated for testing.

    """
    os.chdir('folder')
    for i in range(0, number_files):
        string = '16S_D31-cyt180j_1_data_' + str(i) + '.h5'
        os.remove(string)
    os.chdir('..')
    for i in range(0,len(lista_zipow)):
        os.remove(lista_zipow[i])


def check_dummy_zip(lista_zipow, number_files):
    """
    Checking zip files

    Parameters
    ----------
    lista_zipow : list
    Compressed files list.

    number_files: int
    Number of files generated for testing.
    Returns
    -------
    bool
     True if the number of files is correct, otherwise - False.

    """
    dummy_files(number_files)
    os.chdir('..')
    checkZip('folder', 'nowyDir', '16S_D31-cyt180j_1')
    check_zip=True
    l = list(os.listdir())
    for i in lista_zipow:
        if i not in l:
            check_zip=False
    delete_dummy_files(lista_zipow, number_files)
    return check_zip





#checkZip('dwa','nowyDir','16S_D31-cyt180j_1')
# check_dummy_zip()