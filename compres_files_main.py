from compres import *


def compres_files_main(dir, files_prefix):
    zip_files_lst = zip_files(dir, files_prefix, files_prefix)
    return zip_files_lst
