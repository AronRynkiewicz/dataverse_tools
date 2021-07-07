import math
from zipfile import ZipFile
import os
from os.path import basename

LIMIT = 900

def create_dict(dirName):
   """
    Creates a dictionary with filenames.
    
    Parameters
    ----------
    dirName : string
        The name of the directory where the desired files are located.

    Returns
    ------- 
        Dictionary with dataset name as key and list of files as value.
   """
   d={}
   for folderName, subfolders, filenames in os.walk(dirName):
       for filename in filenames:
           if 'data' in filename:
               file_type = '_'.join(filename.split('_')[:-2])
           else:
               file_type = '_'.join(filename.split('_')[:-1])
           try:
               d[file_type].append(filename)
           except Exception:
               d[file_type] = [filename]

   return d


def zipFilesInDir2(dirName, zipFileName, filter, d, low_range, high_range):
    """
    Creates a compressed files.

    
    dirName : string
        The name of the directory where the desired files are located.

    zipFileName : string
        The name of the compressed file.

    filter : string
        The proper name of the data set.

    d : dictionary
        Dictionary with filenames

    low_range : int
        The number of the first saved file.

    high_range : int
        Last saved file number.
    """
    dataset = filter
    with ZipFile(zipFileName, 'w') as zipObj:
        try:
            d[dataset]
        except KeyError:
            return

        for i in range(low_range, high_range):
            filePath = os.path.join(dirName, d[dataset][i])
            zipObj.write(filePath, basename(filePath))
    zipObj.close()


def zip_files(dirName, zipFileName, filter):
    """
    Check the number of files.

    Parameters
    ----------
    dirName : string
        The name of the directory where the desired files are located.

    zipFileName : string
        The name of the compressed file.

    filter : string
        The proper name of the data set.

     Returns
    -------
        List with the names of the output files.
    """
    lst=[]
    dataset = filter
    d = create_dict(dirName)
    try:
        d[dataset]
    except KeyError:
        return []

    datasets_files_counter = int(len(d[dataset]))
    if (datasets_files_counter < LIMIT):
        zipFilesInDir2(dirName, zipFileName + '.zip', filter, d, 0, len(d[dataset]))
        lst.append(zipFileName + '.zip')
    else:
        number = math.ceil(int(datasets_files_counter) / LIMIT)
        for i in range(0, int(number)):
            previous_value = datasets_files_counter
            datasets_files_counter -= LIMIT
            if datasets_files_counter > 0:
                zipFilesInDir2(dirName, zipFileName + str(i) + '.zip', filter, d, LIMIT * i, (i+1)*LIMIT)
                lst.append(zipFileName + str(i) + '.zip')
            if datasets_files_counter < 0:
                zipFilesInDir2(dirName, zipFileName + str(i) + '.zip', filter, d, LIMIT * i, (LIMIT * i) + previous_value)
                lst.append(zipFileName + str(i) + '.zip')
    return lst