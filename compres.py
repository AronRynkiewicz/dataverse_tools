import math
from zipfile import ZipFile
import os
from os.path import basename
from halo import Halo

ALLOWED_ZIP_SIZE = 1900

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
    d = {}

    for filename in os.listdir(dirName):
        path = os.path.join(os.getcwd(), dirName, filename)
        if os.path.isdir(path):
            continue

        # if "data" in filename:
        #     file_type = "_".join(filename.split("_")[:-2])
        # else:

        file_type = "_".join(filename.split("_")[:-1])
        try:
            d[file_type].append(filename)
        except Exception:
            d[file_type] = [filename]

    return d


def zipFilesInDir2(dirName, zipFileName, filter, d, lst):
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

    lst: list
        List of files to be compressed.

    """
    dataset = filter
    with ZipFile(zipFileName, "w") as zipObj:
        try:
            d[dataset]
        except KeyError:
            return

        for i in range(0, len(lst)):
            filePath = os.path.join(dirName, lst[i])
            zipObj.write(filePath, basename(filePath))
    zipObj.close()


def convert_to_MBs(bytes_value):
    return math.ceil(bytes_value / (1024 ** 2))


def check_if_files_already_exists(list_with_lst_to_zip, zipFileName):
    prev = 0

    files_lst = []
    for i in range(0, len(list_with_lst_to_zip)):
        tmp_zipFileName = (
            zipFileName
            + "_"
            + "img"
            + "_"
            + str(prev + 1)
            + "_"
            + str(prev + len(list_with_lst_to_zip[i]))
            + ".zip"
        )
        files_lst.append(tmp_zipFileName)
        prev += len(list_with_lst_to_zip[i])

    if all([True if i in os.listdir() else False for i in files_lst]):
        return True, files_lst
    else:
        return False, []


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
    lst = []
    lst_mb = []
    lst_size_file = []
    list_with_lst_to_zip = []
    lst_to_zip = []
    remembered_size = 0

    dataset = filter
    d = create_dict(dirName)

    try:
        d[dataset]
    except KeyError:
        print(filter)
        print(d.keys())
        return []

    current_path = os.getcwd()

    os.chdir(dirName)
    for i in range(0, len(d[dataset])):
        size_file = os.stat(d[dataset][i]).st_size
        lst_size_file.append(size_file)
    os.chdir(current_path)

    lst_mb = list(map(convert_to_MBs, lst_size_file))
    d[dataset].sort(key=lambda f: int(f.split("_")[-1].split(".")[0]))

    for i in range(0, len(d[dataset])):
        lst_to_zip.append(d[dataset][i])
        remembered_size += lst_mb[i]

        if remembered_size >= ALLOWED_ZIP_SIZE:
            lst_to_zip.pop()
            lst_to_zip.sort(key=lambda f: int(f.split("_")[-1].split(".")[0]))

            list_with_lst_to_zip.append(lst_to_zip[:])
            lst_to_zip.clear()
            remembered_size = 0
            lst_to_zip.append(d[dataset][i])
            remembered_size += lst_mb[i]

    lst_to_zip.sort(key=lambda f: int(f.split("_")[-1].split(".")[0]))
    list_with_lst_to_zip.append(lst_to_zip[:])

    already_created, files = check_if_files_already_exists(list_with_lst_to_zip, zipFileName)

    if already_created:
        print("Similar zip files found, omitting new ones creation")
        return files

    prev = 0

    print(
        str(len(d[dataset]))
        + " files selected: "
        + list_with_lst_to_zip[0][0]
        + " to "
        + list_with_lst_to_zip[-1][-1]
    )

    print(str(len(list_with_lst_to_zip)) + " zip files will be created")

    for i in range(0, len(list_with_lst_to_zip)):

        file_pos = str(i + 1) + " of " + str(len(list_with_lst_to_zip))
        spinner = Halo(text="Creating zip: " + file_pos, spinner='dots')
        spinner.start()

        tmp_zipFileName = (
            zipFileName
            + "_"
            + "img"
            + "_"
            + str(prev + 1)
            + "_"
            + str(prev + len(list_with_lst_to_zip[i]))
            + ".zip"
        )

        zipFilesInDir2(
            dirName,
            tmp_zipFileName,
            filter,
            d,
            list_with_lst_to_zip[i],
        )
        lst.append(tmp_zipFileName)
        prev += len(list_with_lst_to_zip[i])
        spinner.succeed("Created zip: " + file_pos)

    return lst
