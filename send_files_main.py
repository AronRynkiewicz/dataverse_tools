import os
from compres import zip_files
from tools import *
from urllib.parse import urlparse
from urllib.parse import parse_qs

from main import ZIP_FILES_DESCRIPTION


def send_files_main(api, dir, files_prefix, url):
    parsed_url = urlparse(url)
    DOI = parse_qs(parsed_url.query)["persistentId"][0]

    if get_dataset_id(api, DOI) == -1:
        print("Please check the url, dataset with given DOI does not exists!")
        return

    print("Preparing files...")
    zip_files_list = zip_files(dir, files_prefix, files_prefix)
    print("Done")

    print("Sending zips to dataset...")
    for it, file in enumerate(zip_files_list):
        print("Uploading file #" + str(it))
        code = upload_file_to_dataset(DOI, file, ZIP_FILES_DESCRIPTION)
        print("Status: " + str(code))
    print("Done")

    print("Cleaning...")
    for file in zip_files_list:
        os.remove(file)
    print("Done")
