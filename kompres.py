from zipfile import ZipFile
import os
from os.path import basename


def createDir(dirName):
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

def zipFilesInDir2(dirName, zipFileName, filter):
    d=createDir(dirName)
    with ZipFile(zipFileName, 'w') as zipObj:
        for key in d:
            for n in filter.split(','):
                if (key==n):
                    for i in range(0, len(d[key])):
                        filePath = os.path.join(dirName, d[n][i])
                        zipObj.write(filePath, basename(filePath))
    zipObj.close()

zipFilesInDir2('Nazwafolderu','nowyDir.zip','16S_D31-cyt180j_1')


